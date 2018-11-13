from node import Attribute


class LineStyle(Attribute):
    def __repr__(self):
        return "<LineStyle: {},{},{}>".format(
            self.color, self.type, self.width
        )


class Edge(object):

    def __init__(self, id_, source, target, line_style):
        self.id = id_
        self.source = source
        self.target = target
        self.ls = line_style

    def __repr__(self):
        return '<Edge {}: {}->{}'.format(self.id, self.source, self.target)
