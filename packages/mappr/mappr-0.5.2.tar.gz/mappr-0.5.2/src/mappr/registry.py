from contextvars import ContextVar
from typing import Callable, Dict, List, Optional, Type, TypeVar

from . import exc, mappers, types
from .enums import Strategy


T = TypeVar('T')
TypeConverterList = List[types.TypeConverter]
g_converters: ContextVar[TypeConverterList] = ContextVar('g_converters', default=[])
T_src = TypeVar('T_src')
T_dst = TypeVar('T_dst')


def register(
    src_type: Type,
    dst_type: Type,
    strategy: Strategy = Strategy.CONSTRUCTOR,
    mapping: Optional[types.FieldMapping] = None,
    strict: bool = True
):
    """ Register new converter.

    Args:
        src_type:
        dst_type:
        strategy:
        mapping:
        strict:

    Returns:

    """
    _register_converter(
        types.MappingConverter(
            src_type=src_type,
            dst_type=dst_type,
            mapping=mapping or {},
            strategy=strategy,
        ),
        strict=strict,
    )


def custom_converter(
    src_type: Type[T_src],
    dst_type: Type[T_dst],
    strategy: Strategy = Strategy.CONSTRUCTOR,
    strict: bool = True
):
    """ Decorator for registering a custom conversion functions. """
    def decorator(conversion_fn: Callable[[T_src, types.Values, Strategy], T_dst]):
        _register_converter(
            types.CustomConverter(
                src_type=src_type,
                dst_type=dst_type,
                strategy=strategy,
                custom_converter=conversion_fn,
            ),
            strict=strict,
        )

        return conversion_fn

    return decorator


def _register_converter(converter: types.TypeConverter, strict: bool = True):
    """ Register new converter. """
    existing = find_converter(converter.src_type, converter.dst_type)
    converters = g_converters.get()

    if existing:
        if strict:
            raise exc.ConverterAlreadyExists(converter.src_type, converter.dst_type)
        else:
            converters.remove(existing)

    converters.append(converter)


def register_iso(
    src_type: Type,
    dst_type: Type,
    strategy: Strategy = Strategy.CONSTRUCTOR,
    mapping: Optional[Dict[str, str]] = None,
    strict: bool = True,
):
    mapping = mapping or {}

    if strict:
        if find_converter(src_type, dst_type):
            raise exc.ConverterAlreadyExists(src_type, dst_type)
        if find_converter(dst_type, src_type):
            raise exc.ConverterAlreadyExists(dst_type, src_type)

    register(src_type, dst_type, strategy=strategy, strict=strict, mapping={
        k: mappers.alias(v) for k, v in mapping.items()
    })
    register(dst_type, src_type, strategy=strategy, strict=strict, mapping={
        v: mappers.alias(k) for k, v in mapping.items()
    })


def get_converter(src_type: Type, dst_type: Type[T], strict: bool) -> types.TypeConverter:
    """ Do everything to return a converter or raise if it's not possible.

    In **strict** mode, it will not create an ad-hoc default converter and will
    require the converter to have been registered earlier.
    """
    converter = find_converter(src_type, dst_type)
    if converter:
        return converter
    elif not strict:
        # If not strict, create an ad-hoc converter for the types. This will try
        # to map the properties from `dst_type` to src_type. `dst_types` attributes
        # must be a subset of `src_type` attributes.
        return types.MappingConverter(
            src_type=src_type,
            dst_type=dst_type,
            strategy=Strategy.CONSTRUCTOR,
        )
    else:
        raise exc.NoConverter(src_type, dst_type)


def find_converter(src_type, dst_type) -> Optional[types.TypeConverter]:
    converters = g_converters.get()
    return next(
        (c for c in converters if c.src_type == src_type and c.dst_type == dst_type),
        None
    )
