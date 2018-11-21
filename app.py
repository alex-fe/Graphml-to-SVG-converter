from xml.dom import minidom

import svgwrite

from element import Attribute, Border, Edge, Node


class Graph(object):

    def __init__(self, path):
        self.path = path
        self.svg_path = path.replace('test.graphml', 'output.svg')
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
                Border(**border),
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
        svg = svgwrite.Drawing(filename=self.svg_path, debug=True, profile='full')
        for node in self.nodes.values():
            rect = svg.rect(insert=node.coordinates, size=node.size)
            rect.fill(color=node.color)
            rect.stroke(color=node.border_color, width=node.border.width)
            rect.dasharray(dasharray=node.border.dasharray)
            svg.add(rect)
        for edge in self.edges.values():

        svg.save()
        # import pdb; pdb.set_trace()


if __name__ == '__main__':
    path = "/Users/alexfeldman/CS/Freelance/Graphml_converter/Test_files/test.graphml"
    g = Graph(path)
    g.parse_nodes()
    g.parse_edges()
    g.draw_svg()
