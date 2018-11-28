from mixins import NameMixin, RGBMixin
from element import Point


def test_hex_to_rgb():
    hex_white = "#ffffff"
    hex_black = "#000000"
    assert RGBMixin.hex_to_rgb(hex_white) == 'rgb(255,255,255)'
    assert RGBMixin.hex_to_rgb(hex_black) == 'rgb(0,0,0)'


def test_repr_mixin():
    assert NameMixin in Point.__bases__  # assert inheritance
    point = Point(1, 3)
    assert repr(point) == 'Point'
