from typing import Any, Optional, Type, TypeVar

from . import registry
from .enums import Strategy


T = TypeVar('T')


def convert(
    dst_type: Type[T],
    src_obj: Any,
    strict: bool = True,
    strategy: Optional[Strategy] = None,
    **extra: Any,
) -> T:
    """ Convert an object to a given type.

    Args:
        dst_type:   Target type. This is the type of the return value.
        src_obj:    An object to convert. A registered converter will be used
                    to map between the attributes of this object and the target
                    type.
        strict:     If set to ``False`` and the converter is not found for the
                    given type pair, it will create an ad-hoc one that maps
                    the attributes by their name. Defaults to ``True``
        strategy:   Creation strategy
        extra:      Extra arguments to pass to the converter.

    Returns:
        A newly created instance of ``dst_type`` with values initialized
        from ``src_obj``.
    """
    converter = registry.get_converter(src_obj.__class__, dst_type, strict=strict)
    strategy = strategy or converter.strategy

    return converter.convert(src_obj, strategy, extra)
