import svgwrite


def hex_to_rgb(hex_):
        hex_ = hex_.lstrip('#')
        r, g, b = tuple(int(hex_[i:i + 2], 16) for i in (0, 2, 4))
        return svgwrite.utils.rgb(r, g, b)


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


class Border(Attribute):
    def __init__(self, **kwargs):
        super(Border, self).__init__(self.__class__.__name__, **kwargs)
        if self.type == 'dashed':
            self.dasharray = ['75%', '25%']
        else:
            self.dasharray = None


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
    def size(self):
        return (float(self.geometry.width), float(self.geometry.height))

    @property
    def color(self):
        return hex_to_rgb(self.fill.color)

    @property
    def border_color(self):
        return hex_to_rgb(self.border.color)


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
        return '<Edge {}: {}->{}'.format(self.id, self.source, self.target)
