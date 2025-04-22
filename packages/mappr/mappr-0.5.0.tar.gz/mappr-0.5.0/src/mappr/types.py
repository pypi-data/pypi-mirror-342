import abc
import dataclasses
from typing import Any, Callable, Dict, Generic, Iterator, Optional, Type, TypeVar

from .enums import Strategy


T_src = TypeVar('T_src')
T_dst = TypeVar('T_dst')
Values = Dict[str, Any]
ConverterFn = Callable[[Any], Any]
MappingFn = Callable[[T_src, Values], Any]
FieldMapping = Dict[str, MappingFn]
FieldIterator = Iterator[str]
TestFn = Callable[[Type], bool]


@dataclasses.dataclass
class FieldIter:
    test: TestFn
    iter_factory: Callable[[type], FieldIterator]

    def can_handle(self, any_cls: Type) -> bool:
        # We need to use getattr as using self.test will call test as a method
        # (passing self as first argument). At least mypy reports that.
        # TODO: Look into whether this is just a mypy issue.
        return getattr(self, 'test')(any_cls)

    def make_iterator(self, any_cls: Type) -> FieldIterator:
        return getattr(self, 'iter_factory')(any_cls)


@dataclasses.dataclass
class TypeConverter(abc.ABC, Generic[T_src, T_dst]):
    src_type: Type[T_src]
    dst_type: Type[T_dst]
    strategy: Strategy

    @abc.abstractmethod
    def convert(
        self,
        src_obj: T_src,
        strategy: Optional[Strategy] = None,
        extra: Optional[Values] = None,
    ) -> T_dst:
        ...

    def build_result(
        self,
        values: Values,
        strategy: Optional[Strategy] = None,
    ) -> T_dst:
        strategy = strategy or self.strategy

        if strategy == Strategy.CONSTRUCTOR:
            return self.build_by_constructor(self.dst_type, values)
        else:
            return self.build_by_setattr(self.dst_type, values)

    @staticmethod
    def build_by_constructor(dst_type: Type[T_dst], values: Values) -> T_dst:
        return dst_type(**values)

    @staticmethod
    def build_by_setattr(dst_type: Type[T_dst], values: Values) -> T_dst:
        result = dst_type()
        for name, value in values.items():
            setattr(result, name, value)

        return result


@dataclasses.dataclass
class MappingConverter(TypeConverter[T_src, T_dst]):
    mapping: FieldMapping = dataclasses.field(default_factory=dict)

    def convert(
        self,
        src_obj: T_src,
        strategy: Optional[Strategy] = None,
        extra: Optional[Values] = None,
    ) -> T_dst:
        from . import iterators, mappers

        extra = extra or {}
        values = {}
        for name in iterators.iter_fields(self.dst_type):
            mapping_fn = self.mapping.get(name, mappers.alias(name))

            if mapping_fn != mappers.use_default:
                values[name] = mapping_fn(src_obj, extra)

        return self.build_result(values, strategy)


@dataclasses.dataclass
class CustomConverter(TypeConverter[T_src, T_dst]):
    custom_converter: Callable[[T_src, Values, Strategy], T_dst]

    def convert(
        self,
        src_obj: T_src,
        strategy: Optional[Strategy] = None,
        extra: Optional[Values] = None,
    ) -> T_dst:
        extra = extra or {}
        strategy = strategy or self.strategy

        return self.custom_converter(src_obj, extra, strategy)
