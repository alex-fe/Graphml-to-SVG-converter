from unittest.mock import patch, PropertyMock

import pytest

from element import Arrow, Edge, Geometry, Node, Path, Point, Style


def test_point_coordinates():
    x = 4.0
    y = 54.1
    point = Point(x, y)
    assert isinstance(point.coordinates, tuple)
    assert point.coordinates[0] == x
    assert point.coordinates[1] == y


def test_point_translate():
    x = 4.0
    y = 2.1
    x_mod = 3
    y_mod = 2
    point = Point(x, y)
    point.translate(x_mod, y_mod)
    assert point.x == x + x_mod
    assert point.y == y + y_mod

    point = Point(x, y)
    point.translate(x_mod)
    assert point.x == x + x_mod
    assert point.y == y + x_mod


def test_point_scale():
    x = 4.0
    y = 2.1
    x_mod = 3
    y_mod = 2
    point = Point(x, y)
    point.scale(x_mod, y_mod)
    assert point.x == x * x_mod
    assert point.y == y * y_mod

    point = Point(x, y)
    point.scale(x_mod)
    assert point.x == x * x_mod
    assert point.y == y * x_mod


def test_geometry_size():
    x = 4.0
    y = 54.1
    width = 2.0
    height = 4.534
    geometry = Geometry(width, height, x, y)
    assert isinstance(geometry.size, tuple)
    assert geometry.size[0] == width
    assert geometry.size[1] == height


def test_geometry_center():
    x = 4.0
    y = 54.1
    width = 2.0
    height = 5.0
    geometry = Geometry(width, height, x, y)
    assert isinstance(geometry.center, tuple)
    assert geometry.center[0] == width / 2
    assert geometry.center[1] == height / 2


def test_style_dasharray():
    hex_white = "#ffffff"
    type_ = 'line'
    style = Style(hex_white, type_)
    assert style.dasharray is None

    type_ = 'dashed'
    style = Style(hex_white, type_)
    assert isinstance(style.dasharray, list)
    assert len(style.dasharray) == 2


def test_arrow_draw_source():
    source = 'delta'
    arrow = Arrow(source, None)
    assert arrow.draw_source


def test_arrow_draw_target():
    target = 'delta'
    arrow = Arrow(None, target)
    assert arrow.draw_target


@pytest.mark.skip()
def test_arrow_d():
    arrow = Arrow(None, None)
    origin, base, tip, _ = arrow.d.split()


def test_ref_y():
    arrow = Arrow(None, None)
    assert arrow.ref_y == arrow.height / 2


@pytest.mark.skip("fixture 'self' not found")
def test_node_equality(self):
    x = 4.0
    y = 5.0
    geometry = Geometry(2.0, 3.8, x, y)
    node1 = Node('id', 'key', 'text', 'rect', None, geometry, None, None)
    node2 = Node('id', 'key', 'text', 'rect', None, geometry, None, None)
    assert (
        node1.geometry.x == node2.geometry.x
        and node1.geometry.y == node2.geometry.y
    )
    assert node1 == node2


@pytest.mark.skip("fixture 'self' not found")
def test_node_lt(self):
    geometry = Geometry(2.0, 3.8, 1.3, 2.2)
    node1 = Node('id', 'key', 'text', 'rect', None, geometry, None, None)
    geometry.scale(4)
    node2 = Node('id', 'key', 'text', 'rect', None, geometry, None, None)
    assert node1 < node2


def test_node_coordinates():
    geometry = Geometry(3.8, 2.0, 4.0, 13.21)
    node = Node('id', 'key', 'text', 'rect', None, geometry, None, None)
    assert node.coordinates[0] == node.geometry.x
    assert node.coordinates[1] == node.geometry.y


@pytest.mark.skip("Not yet")
def test_node_location_relation():
    geometry = Geometry(3.8, 2.0, 4.0, 13.21)
    node = Node('id', 'key', 'text', 'rect', None, geometry, None, None)
    # test comparison between non-Node
    with pytest.raises(TypeError):
        node.location_relation(Point)
    # test when width == 0, y == 0
    node.geometry.width = 0.0
    node.geometry.height = 0.0
    geometry.translate(2)
    node2 = Node('id', 'key', 'text', 'rect', None, geometry, None, None)
    x, y = node.location_relation(node2)
    assert x == node.geometry.x
    assert y == node.geometry.y
    # test node left


@patch('element.Edge.end_coordinates', new_callable=PropertyMock)
@patch('element.Edge.start_coordinates', new_callable=PropertyMock)
def test_edge_d(start_coordinates, end_coordinates):
    sc_values = (0, 1)
    ec_values = (10, 5)
    start_coordinates.return_value = sc_values
    end_coordinates.return_value = ec_values
    points = [Point(i, i * 3) for i in range(4)]
    path = Path(points)
    edge = Edge('id_', 'key', None, None, None, path, None)
    coordinates = (
        sc_values + edge.path.points[0].coordinates
        + edge.path.points[1].coordinates + edge.path.points[2].coordinates
        + edge.path.points[3].coordinates + ec_values
    )
    d_ = 'M{},{} L{},{} L{},{} L{},{} L{},{} L{},{}'.format(*coordinates)
    assert edge.d == d_
