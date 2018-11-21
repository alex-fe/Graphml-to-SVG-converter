import sys
from xml.dom import minidom

import svgwrite

from element import Edge, Fill, Geometry, Label, Node, Style, Viewbox


class Graph(object):

    def __init__(self, path, output_path=None):
        self.path = path
        if output_path is None:
            self.svg_path = path.replace('.graphml', '.svg')
        else:
            self.svg_path = output_path
        self.xml = minidom.parse(self.path)
        self.nodes = {}
        self.edges = {}
        self.viewbox = None

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
                .strip()
            )
        except IndexError:
            return

    def add_node(
        self, id_, text='',
        height=10.0, width=10.0, x=0.0, y=0.0,  # Geometry args
        fill_color="#ffffff", transparent=False,  # Fill args
        border_color="#000000", border_type='line', border_width=1.0,  # Border args
        geometry=None, label=None, fill=None, border=None,
        **label_kwargs
    ):
        if geometry is None:
            geometry = Geometry(height, width, x, y)
        if fill is None:
            fill = Fill(fill_color, transparent)
        if border is None:
            border = Style(border_color, border_type, border_width)
        if label is None:
            label = Label(**label_kwargs)

        self.nodes[id_] = Node(id_, text, label, geometry, fill, border)


    def parse_nodes(self):
        nodes = self.xml.getElementsByTagName('node')
        for node in nodes:
            la = self.__get_node_label(node)
            id_ = node.attributes['id'].value
            geometry = self.get_attrs(node, 'y:Geometry')
            fill = self.get_attrs(node, 'y:Fill')
            border = self.get_attrs(node, 'y:BorderStyle')
            label = {
                **self.get_attrs(node, 'y:NodeLabel'),
                **self.get_attrs(node, 'y:SmartNodeLabelModelParameter')
            }
            self.nodes[id_] = Node(
                id_,
                la,
                Label('Label', **label),
                Attribute('Geometry', **geometry),
                Attribute('Fill', **fill),
                Style('Border', **border),
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
                self.nodes[source],
                self.nodes[target],
                Style('Line Style', **line_style),
                Attribute('Path', **linepath),
                Attribute('Arrow', **arrow),
                Attribute('Bend', **bend),
                points
            )

    def create_viewbox(self):
        min_x = sys.maxsize
        min_y = sys.maxsize
        max_x = -sys.maxsize
        max_y = -sys.maxsize
        for node in self.nodes.values():
            if node.coordinates[0] > max_x:
                max_x = node.coordinates[0]
            if node.coordinates[1] > max_y:
                max_y = node.coordinates[1]
            if node.coordinates[0] < min_x:
                min_x = node.coordinates[0]
            if node.coordinates[1] < min_y:
                min_y = node.coordinates[1]
        width = max_x - min_x
        height = max_y - min_y
        self.viewbox = Viewbox(min_x, min_y, width, height)

    def draw_svg(self):
        svg = svgwrite.Drawing(filename=self.svg_path)
        svg.viewbox(**self.viewbox.box)
        for node in self.nodes.values():
            rect = svg.rect(insert=node.coordinates, size=node.size)
            rect.fill(color=node.color)
            rect.stroke(color=node.border_color, width=node.border.width)
            rect.dasharray(dasharray=node.border.dasharray)
            svg.add(rect)
            if node.text:
                label = svgwrite.text.Text(
                    node.text,
                    insert=node.l_coordinates,
                )
                label.fill(color=node.label_color)
                svg.add(label)
        for edge in self.edges.values():
            line = svgwrite.shapes.Line(
                start=edge.start_coordinates, end=edge.end_coordinates
            )
            line.fill(color=edge.color)
            line.stroke(width=edge.line_style.width)
            svg.add(line)
        svg.save()
        # import pdb; pdb.set_trace()


if __name__ == '__main__':
    path = "/Users/alexfeldman/CS/Freelance/Graphml_converter/Test_files/test.graphml"
    g = Graph(path)
    g.parse_nodes()
    g.parse_edges()
    g.create_viewbox()
    g.draw_svg()
