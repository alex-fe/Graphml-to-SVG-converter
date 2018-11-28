import pytest
from mixins import NameMixin, RGBMixin


def test_hex_to_rgb():
    hex_white = "#ffffff"
    hex_black = "#000000"
    assert RGBMixin.hex_to_rgb(hex_white) == 'rgb(255,255,255)'
    assert RGBMixin.hex_to_rgb(hex_black) == 'rgb(0,0,0)'


@pytest.mark.skip()
def test_repr_mixin():
    assert repr(NameMixin) == type(NameMixin)
