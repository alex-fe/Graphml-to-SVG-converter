import os
from xml.dom import minidom


from node import Attribute, Edge, Node


class Graph(object):

    def __init__(self, path):
        self.path = path
        self._svg_path = path.replace('.graphml', '.svg')
        self.xml = minidom.parse(self.path)
        self.nodes = {}
        self.edges = {}

    @staticmethod
    def get_attrs(element, label, i=0):
        try:
            items = element.getElementsByTagName(label)[i].attributes.items()
        except IndexError:
            return {}
        else:
            return {k: v for k, v in items}

    @staticmethod
    def __get_node_label(node):
        try:
            return (
                node
                .getElementsByTagName('y:NodeLabel')[0]
                .childNodes[0]
                .data
            )
        except IndexError:
            return ''

    @property
    def svg_path(self):
        return self._svg_path

    @svg_path.setter
    def svg_path(self, path=None, name=None):
        head, tail = os.path.split(self._svg_path)
        if path is not None:
            head = path
        if name is not None:
            tail = name
        self._svg_path = os.path.join(head, tail)

    def parse_nodes(self):
        nodes = self.xml.getElementsByTagName('node')
        for node in nodes:
            la = self.__get_node_label(node).strip()
            id_ = node.attributes['id'].value
            geometry = self.get_attrs(node, 'y:Geometry')
            fill = self.get_attrs(node, 'y:Fill')
            border = self.get_attrs(node, 'y:BorderStyle')
            label = self.get_attrs(node, 'y:NodeLabel')
            self.nodes[id_] = Node(
                id_,
                la,
                Attribute('Label', **label),
                Attribute('Geometry', **geometry),
                Attribute('Fill', **fill),
                Attribute('Border', **border),
            )

    def parse_edges(self):
        edges = self.xml.getElementsByTagName('edge')
        for edge in edges:
            id_ = edge.attributes['id'].value
            source = edge.attributes['source'].value
            target = edge.attributes['target'].value
            line_style = self.get_attrs(edge, 'y:LineStyle')
            linepath = self.get_attrs(edge, 'y:Path')
            arrow = self.get_attrs(edge, 'y:Arrows')
            bend = self.get_attrs(edge, 'y:BendStyle')
            points = [
                Attribute('Point', **self.get_attrs(p, 'y:Point'))
                for p in edge.getElementsByTagName('y:Point')
            ]
            self.edges[id_] = Edge(
                id_,
                source,
                target,
                Attribute('Line Style', **line_style),
                Attribute('Path', **linepath),
                Attribute('Arrow', **arrow),
                Attribute('Bend', **bend),
                points
            )

    def draw_svg(self):
        pass

if __name__ == '__main__':
    path = "/Users/alexfeldman/CS/Freelance/Graphml_converter/Test_files/test_map_svg_convert.graphml"
    g = Graph(path)
    g.parse_nodes()
    g.parse_edges()
    import pdb; pdb.set_trace()
    # g.export()
