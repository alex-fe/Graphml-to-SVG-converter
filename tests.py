from element import Geometry, Node, Point, Style, Viewbox
from mixins import RGBMixin


def test_hex_to_rgb():
    hex_white = "#ffffff"
    hex_black = "#000000"
    assert RGBMixin.hex_to_rgb(hex_white) == 'rgb(255,255,255)'
    assert RGBMixin.hex_to_rgb(hex_black) == 'rgb(0,0,0)'


def test_viewbox_box():
    min_x = 3.0
    min_y = 4.5
    width = 2.0
    height = 4.534
    vb = Viewbox(min_x, min_y, width, height)
    assert vb.box['minx'] == min_x
    assert vb.box['miny'] == min_y
    assert vb.box['width'] == width
    assert vb.box['height'] == height


def test_point_coordinates():
    x = 4.0
    y = 54.1
    point = Point(x, y)
    assert isinstance(point.coordinates, tuple)
    assert point.coordinates[0] == x
    assert point.coordinates[1] == y


def test_geometry_size():
    x = 4.0
    y = 54.1
    width = 2.0
    height = 4.534
    geometry = Geometry(height, width, x, y)
    assert isinstance(geometry.size, tuple)
    assert geometry.size[0] == width
    assert geometry.size[1] == height


def test_style_dasharray():
    hex_white = "#ffffff"
    type_ = 'line'
    style = Style(hex_white, type_)
    assert style.dasharray is None

    type_ = 'dashed'
    style = Style(hex_white, type_)
    assert isinstance(style.dasharray, list)
    assert len(style.dasharray) == 2


def test_node_coordinates():
    x = 4.0
    y = 5.0
    width = 2.0
    height = 3.8
    geometry = Geometry(height, width, x, y)
    node = Node(None, None, None, 'rect', None, geometry, None, None)
    assert node.coordinates[0] == node.geometry.x + (width / 2)
    assert node.coordinates[1] == node.geometry.y + (height / 2)

    node = Node(None, None, None, None, None, geometry, None, None)
    assert node.coordinates[0] == node.geometry.x
    assert node.coordinates[1] == node.geometry.y
