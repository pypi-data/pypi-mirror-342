import dataclasses

import mappr


@dataclasses.dataclass
class Src:
    text: str = 'hello'
    num: int = 10


@dataclasses.dataclass
class Dst:
    text: str
    num: int = 20


class EmptyConstructor:
    def __init__(self):
        self.text = 'hi'
        self.num = 30


@mappr.field_iterator(test=lambda any_cls: issubclass(any_cls, EmptyConstructor))
def empty_constructor_support(any_cls: EmptyConstructor) -> mappr.FieldIterator:
    yield from ['text', 'num']


def test_auto_generated_converter(scoped_register):
    mappr.register(Src, Dst)

    assert mappr.convert(Dst, Src()) == Dst(text='hello', num=10)


def test_use_default(scoped_register):
    mappr.register(Src, Dst, mapping=dict(num=mappr.use_default))

    assert mappr.convert(Dst, Src()) == Dst(text='hello', num=20)


def test_can_use_setattr_strategy(scoped_register):
    mappr.register(Src, EmptyConstructor)

    result = mappr.convert(EmptyConstructor, Src(), strategy=mappr.Strategy.SETATTR)
    assert result.text == 'hello'
    assert result.num == 10
