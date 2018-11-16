class Attribute(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_args(self, as_string=False):
        args = self.__dict__.keys()
        if as_string:
            return ', '.join(args)
        return args


class Node(object):

    def __init__(self, id_, label, geometry, fill, border):
        self.id = id_
        self.label = label
        self.geometry = geometry
        self.fill = fill
        self.border = border

    def __repr__(self):
        return '<Node {}>'.format(self.id)


class Edge(object):

    def __init__(self, id_, source, target, line_style):
        self.id = id_
        self.source = source
        self.target = target
        self.ls = line_style

    def __repr__(self):
        return '<Edge {}: {}->{}'.format(self.id, self.source, self.target)
