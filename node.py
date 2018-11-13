class Attribute(object):
    def __init__(self, *args):
        for k, v in args:
            setattr(self, k, v)


class Geometry(Attribute):

    def __repr__(self):
        return "<Geo: {},{},{},{}>".format(
            self.height, self.width, self.x, self.y
        )


class Fill(Attribute):

    def __repr__(self):
        return "<Fill: {},{}>".format(self.color, self.transparent)


class Border(Attribute):

    def __repr__(self):
        return "<Border: {},{},{}>".format(self.color, self.type, self.width)


class Label(Attribute):

    def __repr__(self):
        return "<Label: {}>".format(self.label)


class Node(object):

    def __init__(self, id_, label, geometry, fill, border):
        self.id = id_
        self.label = label
        self.geometry = geometry
        self.fill = fill
        self.border = border

    def __repr__(self):
        return '<Node {}>'.format(self.id)
