import sys
from xml.dom import minidom

import svgwrite

from .element import (
    Arrow, Edge, Fill, Geometry, Label, Node, Path, Point, Style, Viewbox
)
from .mixins import NameMixin


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
    def get_attrs(element, tag_name, i=0):
        """Get attributes from tagged elementself. If element not found, or element
        has no attributes, return empty dictionary.
        Args:
            element (xml.element): Element to search within.
            tag_name (str): Wanted child element's tag name.
            i (int): index of which element if more than one. Default is 0.
        Returns:
            If successfull, return populated dictionary.
        """
        try:
            items = element.getElementsByTagName(tag_name)[i].attributes.items()
        except IndexError:
            return {}
        else:
            return {k: v for k, v in items}

    @staticmethod
    def get_node_text(node):
        """Get text from node's 'y:NodeLabel' parameter.
        Args:
            node (xml.element): Node to search within.
        Returns:
            If successfull, return text. Else, return None.
        """
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
            path = Path(points, sx, sy, tx, ty)
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
            for var_name in Geometry.__init__.__code__.co_varnames:
                if var_name in label:
                    label['l_{}'.format(var_name)] = label.pop(var_name)
            if 'xml:space' in label.keys():
                label['xml_space'] = label.pop('xml:space')
            self.add_node(
                id_, data['key'], text, shape, geometry['height'],
                geometry['width'], geometry['x'], geometry['y'],
                fill['color'], fill['transparent'], border['color'], border['type'],
                border['width'], **label
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
            points = [
                Point(**self.get_attrs(edge, 'y:Point', i=i))
                for i, p in enumerate(edge.getElementsByTagName('y:Point'))
            ]
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
            if node.coordinates[0] + node.geometry.width > max_x:
                max_x = node.coordinates[0] + node.geometry.width
            if node.coordinates[1] + node.geometry.height > max_y:
                max_y = node.coordinates[1] + node.geometry.height
            if node.coordinates[0] < min_x:
                min_x = node.coordinates[0]
            if node.coordinates[1] < min_y:
                min_y = node.coordinates[1]
        min_x -= Viewbox.padding
        min_y -= Viewbox.padding
        max_x += Viewbox.padding
        max_y += Viewbox.padding
        width = max_x - min_x
        height = max_y - min_y
        self.viewbox = Viewbox(min_x, min_y, width, height)

    def adjust(self):
        if self.viewbox is None:
            self.create_viewbox()
        for node in self.nodes.values():
            node.geometry.translate(-self.viewbox.x, -self.viewbox.y)
        for edge in self.edges.values():
            for point in edge.path.points:
                point.translate(-self.viewbox.x, -self.viewbox.y)

    def draw_svg(self):
        svg = svgwrite.Drawing(filename=self.svg_path, size=self.viewbox.size)
        for edge in self.edges.values():
            path = svg.path(d=edge.d)
            path.stroke(color=edge.color, width=edge.line_style.width)
            path.fill(color="rgb(255,255,255)", opacity=0.0)
            for pos, draw in zip(('start', 'end'), edge.arrow.draw):
                if draw:
                    arrow = svg.marker(
                        id='arrow_{}_{}'.format(edge.id, pos),
                        refX=edge.arrow.width / 2, refY=edge.arrow.ref_y,
                        size=edge.arrow.size,
                        orient='auto',
                        markerUnits='strokeWidth'
                    )
                    # FIXME: arrow needs to clip top edge.arrow.width / 2 is not the solution
                    tip = svg.path(d=edge.arrow.d, fill=edge.color)
                    arrow.add(tip)
                    svg.defs.add(arrow)
                    path['marker-{}'.format(pos)] = arrow.get_funciri()
            svg.add(path)
        for node in self.nodes.values():
            group = svgwrite.container.Group(id=node.key)
            rect = svg.rect(
                insert=node.coordinates, size=node.size, id=node.id, rx=node.rx,
                ry=node.ry
            )
            rect.fill(color=node.color)
            rect.stroke(color=node.border.color, width=node.border.width)
            rect.dasharray(dasharray=node.border.dasharray)
            group.add(rect)
            if node.text:
                label = svg.text(node.text, insert=node.label_coordinates)
                label['alignment-baseline'] = node.label.alignment
                label['xml:space'] = 'preserve'
                label.fill(color=node.label.color)
                group.add(label)
            svg.add(group)
        svg.save()

    def run(self):
        self.parse_nodes()
        self.parse_edges()
        self.adjust()
        self.draw_svg()
