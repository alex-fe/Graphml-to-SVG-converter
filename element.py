from mixins import NameMixin, RGBMixin


class Viewbox(NameMixin):
    def __init__(self, min_x=0.0, min_y=0.0, width=0.0, height=0.0):
        self.minx = float(min_x)
        self.miny = float(min_y)
        self.width = float(width)
        self.height = float(height)

    @property
    def box(self):
        return self.__dict__


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


class Geometry(Point, NameMixin):

    def __init__(self, height, width, x, y):
        super(Geometry, self).__init__(x, y)
        self.height = float(height)
        self.width = float(width)

    @property
    def size(self):
        return (self.width, self.height)


class Fill(NameMixin, RGBMixin):

    def __init__(self, color, transparent):
        self.color = color
        self.transparent = transparent


class Style(NameMixin, RGBMixin):

    def __init__(self, color, type_, width=1.0, smoothed=None):
        self._color = color
        self.type = type_
        self.width = float(width)
        self.bend_smoothing = smoothed

    @property
    def dasharray(self):
        if self.type == 'dashed':
            return [10, 2]
        else:
            return None

    @property
    def color(self):
        return self.hex_to_rgb(self._color)


class Label(Geometry, NameMixin, RGBMixin):

    def __init__(
        self, alignment="center", autoSizePolicy="content",
        fontFamily="Dialog", fontSize=6.0, fontStyle="plain",
        textColor="#000000", visible="true",
        hasBackgroundColor="false", hasLineColor="false",
        horizontalTextPosition="center", verticalTextPosition="center",
        height=10.0, width=10.0, x=0.0, y=0.0,
        iconTextGap=4.0, modelName="custom",
    ):
        super(Label, self).__init__(height, width, x, y)
        self.alignment = alignment
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

    @property
    def color(self):
        return self.hex_to_rgb(self.text_color)


class Path(NameMixin):
    def __init__(self, sx, sy, tx, ty, points):
        self.sx = sx
        self.sy = sy
        self.tx = tx
        self.ty = ty
        self.points = points


class Arrow(NameMixin):
    def __init__(self, source, target):
        self.source = source
        self.target = target


class Node(RGBMixin):

    __top_left_shapes = 'rect'

    def __init__(self, id_, key, text, shape, label, geometry, fill, border):
        self.id = id_
        self.text = text
        self.shape = shape
        self.key = key
        self.label = label
        self.geometry = geometry
        self.fill = fill
        self.border = border

    def __repr__(self):
        return '<Node {}>'.format(self.id)

    def __str__(self):
        return self.text

    @property
    def coordinates(self):
        if self.shape in self.__top_left_shapes:
            x = self.geometry.x
            y = self.geometry.y
            return (x + (self.geometry.width / 2), y + (self.geometry.height / 2))
        else:
            return self.geometry.coordinates

    @property
    def color(self):
        return self.hex_to_rgb(self.fill.color)


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
        return self.source.coordinates

    @property
    def end_coordinates(self):
        return self.target.coordinates

    @property
    def color(self):
        return self.line_style.color
