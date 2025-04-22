from dataclasses import asdict, dataclass

import pytest

import mappr


@dataclass
class Src:
    text: str = 'hello'
    num: int = 10


@dataclass
class Dst:
    content: str = 'world'
    count: int = 20


def test_can_convert_src_to_dst(scoped_register):
    mappr.register_iso(Src, Dst, mapping=dict(content='text', count='num'))

    src = Src()
    result = mappr.convert(Dst, src)

    expected = Dst(content='hello', count=10)
    assert asdict(result) == asdict(expected)


def test_can_convert_dst_to_src(scoped_register):
    mappr.register_iso(Src, Dst, mapping=dict(content='text', count='num'))

    dst = Dst()
    result = mappr.convert(Src, dst)

    expected = Src(text='world', num=20)
    assert asdict(result) == asdict(expected)


def test_cannot_register_converter_twice_for_the_same_types(scoped_register):
    mappr.register(Src, Dst, mapping=dict(
        content=mappr.alias('text'),
        count=mappr.alias('num'),
    ))

    with pytest.raises(mappr.ConverterAlreadyExists):
        mappr.register(Src, Dst, mapping=dict(
            content=mappr.alias('text'),
            count=mappr.alias('num'),
        ))


def test_can_register_converter_twice_in_non_strict_mode(scoped_register):
    mappr.register(Src, Dst, mapping=dict(
        content=mappr.alias('text'),
        count=mappr.alias('num'),
    ))
    mappr.register(Src, Dst, strict=False, mapping=dict(
        content=mappr.alias('text'),
        count=mappr.alias('num'),
    ))


def test_cannot_register_iso_converter_twice_for_the_same_types(scoped_register):
    mappr.register_iso(Src, Dst, mapping=dict(content='text', count='num'))

    with pytest.raises(mappr.ConverterAlreadyExists):
        mappr.register_iso(Src, Dst, mapping=dict(content='text', count='num'))


def test_cannot_register_iso_if_normal_converter_already_exists(scoped_register):
    mappr.register(Src, Dst, mapping=dict(
        content=mappr.alias('text'),
        count=mappr.alias('num'),
    ))

    with pytest.raises(mappr.ConverterAlreadyExists):
        mappr.register_iso(Src, Dst, mapping=dict(content='text', count='num'))


def test_cannot_register_iso_if_reverse_converter_already_exists(scoped_register):
    mappr.register(Dst, Src, mapping=dict(
        content=mappr.alias('text'),
        count=mappr.alias('num'),
    ))

    with pytest.raises(mappr.ConverterAlreadyExists):
        mappr.register_iso(Src, Dst, mapping=dict(content='text', count='num'))


def test_can_register_iso_converter_twice_in_non_strict_mode(scoped_register):
    mappr.register_iso(Src, Dst, strict=False, mapping=dict(content='text', count='num'))
    mappr.register_iso(Src, Dst, strict=False, mapping=dict(content='text', count='num'))
