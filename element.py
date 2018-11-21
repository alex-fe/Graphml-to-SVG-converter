import svgwrite


class RGBMixin(object):

    def hex_to_rgb(hex_):
            hex_ = hex_.lstrip('#')
            r, g, b = tuple(int(hex_[i:i + 2], 16) for i in (0, 2, 4))
            return svgwrite.utils.rgb(r, g, b)


class Viewbox(object):
    """Specify a rectangle in user space (no units allowed) which should be
    mapped to the bounds of the viewport established by the given element.
        Parameters:
        minx (number) – left border of the viewBox
        miny (number) – top border of the viewBox
        width (number) – width of the viewBox
        height (number) – height of the viewBox
    """

    def __init__(self, min_x=0, min_y=0, width=0, height=0):
        self.minx = min_x
        self.miny = min_y
        self.width = width
        self.height = height

    @property
    def box(self):
        return self.__dict__


class Point(object):

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    @property
    def coordinates(self):
        return (self.x, self.y)


class Geometry(Point):

    def __init__(self, height, width, x, y):
        super(Geometry, self).__init__(x, y)
        self.height = float(height)
        self.width = float(width)

        @property
        def size(self):
            return (self.width, self.height)


class Fill(RGBMixin):

    def __init__(self, color, transparent):
        self.color = color
        self.transparent = transparent


class Style(RGBMixin):

    def __init__(self, color, type_, width, smoothed=None):
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


class Label(Geometry, RGBMixin):

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


class Path(object):
    def __init__(self, sx, sy, tx, ty, points):
        self.sx = sx
        self.sy = sy
        self.tx = tx
        self.ty = ty
        self.points = points


class Arrow(object):
    def __init__(self, source, target):
        self.source = source
        self.target = target


class Node(RGBMixin):

    __top_left_shapes = 'rect'

    def __init__(self, id_, key, text, shape, label, geometry, fill, border):
        self.id = id_
        self.text = text
        self.shape = 'rect'
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
            y = self.geometry.x
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
