import svgwrite


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


class Attribute(object):
    def __init__(self, name, **kwargs):
        self.__name__ = name
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return '<{}>'.format(str(self))

    def __str__(self):
        return self.__name__

    def get_args(self, as_string=False):
        args = self.__dict__.keys()
        if as_string:
            return ', '.join(args)
        return args


class Style(Attribute):
    def __init__(self, name, **kwargs):
        super(Style, self).__init__(self.__class__.__name__, **kwargs)
        if self.type == 'dashed':
            self.dasharray = [10, 2]
        else:
            self.dasharray = None


class Label(Attribute):
    def __init__(self, name, **kwargs):
        super(Label, self).__init__(self.__class__.__name__, **kwargs)
        if not hasattr(self, 'fontFamily'):
            self.fontFamily = 'san serif'
        if not hasattr(self, 'fontSize'):
            self.fontSize = 12
        if not hasattr(self, 'textColor'):
            self.textColor = "#000000"
        self.x_up = float(getattr(self, 'upX', 0))
        self.y_up = float(getattr(self, 'upY', 0))

    @property
    def size(self):
        return (float(self.width), float(self.height))

class Node(object):

    def __init__(self, id_, text, label, geometry, fill, border):
        self.id = id_
        self.text = text
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
        return (float(self.geometry.x), float(self.geometry.y))

    @property
    def l_coordinates(self):
        return (
            self.coordinates[0] + self.label.x_up,
            self.coordinates[1] + self.label.y_up
        )

    property
    def true_coordinates(self):
        if True:
            return (
                self.coordinates[0] + (float(self.geometry.width) / 2),
                self.coordinates[1] + (float(self.geometry.height) / 2),
            )
        else:
            return self.coordinates

    @property
    def size(self):
        return (float(self.geometry.width), float(self.geometry.height))

    @property
    def color(self):
        return hex_to_rgb(self.fill.color)

    @property
    def border_color(self):
        return hex_to_rgb(self.border.color)

    @property
    def label_color(self):
        return hex_to_rgb(self.label.textColor)


class Edge(object):

    def __init__(
        self, id_, source, target, line_style, path, arrow, bend, points
    ):
        self.id = id_
        self.source = source
        self.target = target
        self.line_style = line_style
        self.path = path
        self.points = points
        self.bend = bend
        self.arrow = arrow

    def __repr__(self):
        return '<Edge {}: {}->{}'.format(
            self.id, self.source.id, self.target.id
        )

    @property
    def start_coordinates(self):
        return self.source.coordinates

    @property
    def end_coordinates(self):
        return self.target.coordinates

    @property
    def color(self):
        return hex_to_rgb(self.line_style.color)
