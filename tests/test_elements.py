from unittest.mock import patch

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


@pytest.mark.skip("coordinates method not set")
def test_node_coordinates():
    x = 4.0
    y = 5.0
    width = 2.0
    height = 3.8
    geometry = Geometry(height, width, x, y)
    node = Node('id', 'key', 'text', 'rect', None, geometry, None, None)
    assert node.coordinates[0] == node.geometry.x + (width / 2)
    assert node.coordinates[1] == node.geometry.y + (height / 2)

    node = Node('id', 'key', 'text', 'circle', None, geometry, None, None)

    assert node.coordinates[0] == node.geometry.x
    assert node.coordinates[1] == node.geometry.y


@pytest.mark.skip("coordinates method not set")
def test_edge_coordinates():
    x = 4.0
    y = 5.0
    geometry = Geometry(2, 3, x, y)
    source_node = Node('id', 'key', 'text', 'rect', None, geometry, None, None)

    geometry.translate(4)
    target_node = Node('id', 'key', 'text', 'rect', None, geometry, None, None)
    edge = Edge('id_', 'key', source_node, target_node, None, None, None)

    assert edge.start_coordinates == source_node.coordinates
    assert edge.end_coordinates == target_node.coordinates


@pytest.mark.skip("coordinates method not set")
def test_edge_d(start_coordinates, end_coordinates):
    points = [Point(i, i * 3) for i in range(4)]
    path = Path(points)
    edge = Edge('id_', 'key', None, None, None, path, None)
    coordinates = (
        start_coordinates + edge.path.points[0] + edge.path.points[1]
        + edge.path.points[2] + edge.path.points[3] + end_coordinates
    )
    assert (
        edge.d == 'M{}, {} L{}, {} L{}, {} L{}, {} L{}, {} L{}, {}'.format(*coordinates)
    )
