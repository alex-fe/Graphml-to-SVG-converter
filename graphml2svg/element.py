import functools

from mixins import NameMixin, RGBMixin


class Point(NameMixin):

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    @property
    def coordinates(self):
        return (self.x, self.y)

    def translate(self, x, y=None):
        if y is None:
            y = x
        self.x += x
        self.y += y

    def scale(self, x, y=None):
        if y is None:
            y = x
        self.x *= x
        self.y *= y


class Geometry(Point, NameMixin):

    def __init__(self, width, height, x, y):
        super(Geometry, self).__init__(x, y)
        self.width = float(width)
        self.height = float(height)

    @property
    def size(self):
        return (self.width, self.height)

    @property
    def center(self):
        return (self.width / 2, self.height / 2)


class Viewbox(Geometry, NameMixin):

    padding = 20

    def __init__(self, min_x=0.0, min_y=0.0, width=0.0, height=0.0):
        super(Viewbox, self).__init__(width, height, min_x, min_y)
        self.sx = 2.0
        self.sy = 2.0


class Fill(NameMixin, RGBMixin):

    def __init__(self, color, color2=None, transparent=False, hasColor=False):
        self.color = color
        self.color2 = color2
        self.transparent = transparent
        self.has_color = hasColor


class Style(NameMixin, RGBMixin):

    def __init__(self, color, type_, width=1.0, smoothed=None):
        self._color = color
        self.type = type_
        self.width = float(width)
        self.bend_smoothing = smoothed

    @property
    def dasharray(self):
        if self.type == 'dashed':
            return [15, 2]
        else:
            return None

    @property
    def color(self):
        return self.hex_to_rgb(self._color)


class Label(Geometry, NameMixin, RGBMixin):

    alignment_dict = {'center': 'middle'}

    def __init__(
        self, alignment="center", autoSizePolicy="content",
        fontFamily="Dialog", fontSize=6.0, fontStyle="plain",
        textColor="#000000", visible="true",
        hasBackgroundColor="false", hasLineColor="false",
        horizontalTextPosition="center", verticalTextPosition="center",
        height=10.0, width=10.0, x=0.0, y=0.0,
        iconTextGap=4.0, modelName="custom",
        **kwargs
    ):
        super(Label, self).__init__(width, height, x, y)
        self.alignment = self.alignment_dict.get(alignment, 'middle')
        self.auto_size_policy = autoSizePolicy
        self.font = fontFamily
        self.font_size = fontSize
        self.font_style = fontStyle
        self.text_color = textColor
        self.visible = visible
        self.has_background_color = hasBackgroundColor
        self.has_line_color = hasLineColor
        self.horizontal_text_position = horizontalTextPosition
        self.vertical_text_position = verticalTextPosition
        self.icon_text_gap = iconTextGap
        self.model_name = modelName
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def color(self):
        return self.hex_to_rgb(self.text_color)


class Path(NameMixin):
    def __init__(self, points, sx=0.0, sy=0.0, tx=0.0, ty=0.0):
        self.points = points
        self.sx = sx
        self.sy = sy
        self.tx = tx
        self.ty = ty


class Arrow(Geometry):

    arrows = ['standard', 'delta', 'white_delta', 'plain']

    def __init__(self, source, target, x=0.5, y=0.5, width=3.0, height=2.0):
        super(Arrow, self).__init__(width, height, x, y)
        self.source = source
        self.target = target

    @property
    def draw(self):
        return (self.draw_source, self.draw_target)

    @property
    def draw_source(self):
        return self.source in self.arrows

    @property
    def draw_target(self):
        return self.target in self.arrows

    @property
    def d(self):
        origin_x = 0.0
        origin_y = 0.0
        return 'M{0},{1} L{0},{2} L{3},{4} Z'.format(
            origin_x, origin_y, self.height, self.width, self.ref_y
        )

    @property
    def ref_y(self):
        return self.height / 2


@functools.total_ordering
class Node(RGBMixin):

    _padding = 2

    def __init__(self, id_, key, text, shape, label, geometry, fill, border):
        self.id = id_
        self.text = text
        self.shape = shape
        self.key = key
        self.label = label
        self.geometry = geometry
        self.fill = fill
        self.border = border
        self.rx = 6.0
        self.ry = 6.0

    def __repr__(self):
        return '<Node {}>'.format(self.id)

    def __str__(self):
        return self.text

    def __eq__(self, node):
        if not isinstance(node, Node):
            return TypeError('Can only compare type Node to type Node.')
        return (
            self.geometry.x == node.geometry.x
            and self.geometry.y == node.geometry.y
        )

    def __lt__(self, node):
        if not isinstance(node, Node):
            return TypeError('Can only compare type Node to type Node.')
        if self.geometry.y == node.geometry.y:
            return self.geometry.y < node.geometry.y
        else:
            return self.geometry.x < node.geometry.x

    @property
    def coordinates(self):
        return self.geometry.coordinates

    @property
    def label_coordinates(self):
        return (
            self.geometry.x
            + self.label.width
            + float(getattr(self.label, 'upX', 0)),
            self.geometry.y
            + self.label.height
            + float(getattr(self.label, 'upY', 0))
        )

    @property
    def color(self):
        return self.hex_to_rgb(self.fill.color)

    @property
    def size(self):
        return self.geometry.size

    def location_relation(self, node):
        if not isinstance(node, Node):
            raise TypeError('Argument must be of type Node.')

        if self.geometry.width:
            x_bounds_min = self.geometry.x + (self.geometry.width / 3)
            x_bounds_max = self.geometry.x + (self.geometry.width * 2 / 3)
            if node.geometry.x < x_bounds_min:  # Node left of
                x = self.geometry.x - self._padding
            elif x_bounds_min < node.geometry.x < x_bounds_max:   # Node centered
                x = self.geometry.x + self.geometry.center[0]
            else:  # Node right of
                x = self.geometry.x + self.geometry.width + self._padding
        else:
            x = self.geometry.x

        if self.geometry.height:
            y_bounds_min = self.geometry.height / 3
            y_bounds_max = self.geometry.height * 2 / 3
            if node.geometry.y < y_bounds_min:  # Node above
                y = self.geometry.y + self.height - self._padding
            elif y_bounds_min < node.geometry.y < y_bounds_max:  # Node centered
                y = self.geometry.y + self.geometry.center[1]
            else:  # Node below
                y = self.geometry.y + self._padding
        else:
            y = self.geometry.y

        return (x, y)


class Edge(object):

    def __init__(self, id_, key, source, target, line_style, path, arrow):
        self.id = id_
        self.key = key
        self.source = source
        self.target = target
        self.line_style = line_style
        self.path = path
        self.arrow = arrow

    def __repr__(self):
        return '<Edge {} {}->{}>'.format(self.id, self.source.id, self.target.id)

    @property
    def start_coordinates(self):
        return self.source.location_relation(self.target)

    @property
    def end_coordinates(self):
        return self.target.location_relation(self.source)

    @property
    def color(self):
        return self.line_style.color

    @property
    def d(self):
        data_str = 'M{},{} '.format(*self.start_coordinates)
        for point in self.path.points:
            data_str += 'L{},{} '.format(*point.coordinates)
        data_str += 'L{},{}'.format(*self.end_coordinates)
        return data_str
