import sys
from xml.dom import minidom

import svgwrite

from element import (
    Arrow, Edge, Fill, Geometry, Label, Node, Path, Style, Viewbox
)
from mixins import NameMixin


class Graph(NameMixin):

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
    def get_node_text(node):
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
        self, id_, key=None, text='', shape=None,
        height=10.0, width=10.0, x=0.0, y=0.0,
        fill_color="#ffffff", transparent=False,
        border_color="#000000", border_type='line', border_width=1.0,
        geometry=None, label=None, fill=None, border=None,
        **label_kwargs
    ):
        if geometry is None:
            geometry = Geometry(width, height, x, y)
        if fill is None:
            fill = Fill(fill_color, transparent)
        if border is None:
            border = Style(border_color, border_type, border_width)
        if label is None:
            label = Label(**label_kwargs)
        self.nodes[id_] = Node(id_, key, text, shape, label, geometry, fill, border)

    def add_edge(
        self, id_, key=None, source='', target='',
        edge_color="#000000", edge_type='line', width=1.0, smoothed=False,
        sx=0.0, sy=0.0, tx=0.0, ty=0.0, points=[],
        arrow_source=None, arrow_target='delta',
        line_style=None, path=None, arrow=None
    ):
        if line_style is None:
            line_style = Style(edge_color, edge_type, width, smoothed)
        if path is None:
            path = Path(sx, sy, tx, ty, points)
        if arrow is None:
            arrow = Arrow(arrow_source, arrow_target)
        self.edges[id_] = Edge(
            id_, key, self.nodes.get(source), self.nodes.get(target), line_style,
            path, arrow
        )

    def parse_nodes(self):
        nodes = self.xml.getElementsByTagName('node')
        for node in nodes:
            id_ = node.attributes['id'].value
            text = self.get_node_text(node)
            data = self.get_attrs(node, 'data')
            geometry = self.get_attrs(node, 'y:Geometry')
            fill = self.get_attrs(node, 'y:Fill')
            border = self.get_attrs(node, 'y:BorderStyle')
            shape = 'ellipse'
            label = {
                **self.get_attrs(node, 'y:NodeLabel'),
                **self.get_attrs(node, 'y:SmartNodeLabelModelParameter')
            }
            self.add_node(
                id_, data['key'], text, shape, geometry['height'],
                geometry['width'], geometry['x'], geometry['y'],
                fill['color'], fill['transparent'], border['color'], border['type'],
                border['width'],
            )

    def parse_edges(self):
        edges = self.xml.getElementsByTagName('edge')
        for edge in edges:
            id_ = edge.attributes['id'].value
            data = self.get_attrs(edge, 'data')
            source = edge.attributes['source'].value
            target = edge.attributes['target'].value
            ls = self.get_attrs(edge, 'y:LineStyle')
            bend = self.get_attrs(edge, 'y:BendStyle')
            path = self.get_attrs(edge, 'y:Path')
            arrow = self.get_attrs(edge, 'y:Arrows')
            points = []
            # try:
            #     points = [
            #         Point(**self.get_attrs(p, 'y:Point'))
            #         for p in edge.getElementsByTagName('y:Point')
            self.add_edge(
                id_, data['key'], source, target, ls['color'], ls['type'],
                ls['width'], bend['smoothed'], path['sx'], path['sy'], path['tx'],
                path['ty'], points, arrow['source'], arrow['target']
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
            ellipse = svg.ellipse(center=node.coordinates, r=node.size, id=node.id)
            ellipse.fill(color=node.color)
            ellipse.stroke(color=node.border.color, width=node.border.width)
            ellipse.dasharray(dasharray=node.border.dasharray)
            svg.add(ellipse)
            if node.text:
                label = svg.text(node.text, insert=node.label.coordinates)
                label.fill(color=node.label.color)
                svg.add(label)
        for edge in self.edges.values():
            line = svg.line(
                start=edge.start_coordinates, end=edge.end_coordinates
            )
            line.fill(color=edge.color)
            line.stroke(width=edge.line_style.width)
            svg.add(line)
        svg.save()
        # import pdb; pdb.set_trace()


if __name__ == '__main__':
    path = "/Users/alexfeldman/CS/Freelance/Graphml_converter/tests/Test_files/test.graphml"
    g = Graph(path)
    g.parse_nodes()
    g.parse_edges()
    g.create_viewbox()
    g.draw_svg()
