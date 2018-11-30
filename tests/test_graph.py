import os
from unittest.mock import patch

import pytest

from graphml2svg import Edge, Geometry, Graph, Node


class TestGraph:

    def setup(self):
        self.path = os.path.join(os.path.dirname(__file__), 'test.graphml')
        self.graph = Graph(self.path)
        self.node_id = 'Test Node Id'
        self.edge_id = 'Test Edge Id'

    def test_output_path(self):
        assert os.path.splitext(self.graph.svg_path)[1] == '.svg'
        assert self.graph.svg_path == self.path.replace('.graphml', '.svg')

        output_path = 'another/path/to/file.svg'
        g = Graph(self.path, output_path)
        assert g.svg_path == output_path

    def test_set_graph_attrs(self):
        graph_xml = self.graph.xml.getElementsByTagName('graph')[0]
        attribute = ('test', 'test_val')
        graph_xml.setAttribute(*attribute)
        assert attribute in graph_xml.attributes.items()

        self.graph._set_graph_attrs()
        assert getattr(self.graph, attribute[0]) == attribute[1]

    def test_get_attrs(self):
        node = self.graph.xml.getElementsByTagName('node')[0]
        attribute = 'data'
        assert node.getElementsByTagName(attribute)
        assert self.graph.get_attrs(node, attribute)

        attribute = 'not in node'
        assert not node.getElementsByTagName(attribute)
        assert not self.graph.get_attrs(node, attribute)

    @pytest.mark.skip()
    def test_get_node_text(self):
        node = self.graph.xml.getElementsByTagName('node')[0]

    def test_add_node(self):
        assert not self.graph.nodes
        self.graph.add_node(self.node_id)
        assert self.graph.nodes
        assert isinstance(self.graph.nodes[self.node_id], Node)

    def test_add_edge(self):
        assert not self.graph.edges
        geometry = Geometry(2, 3, 4, 23)
        n1 = Node('n1', 'key', 'text', 'rect', None, geometry, None, None)
        geometry.translate(2)
        n2 = Node('n2', 'key', 'text', 'rect', None, geometry, None, None)
        self.graph.nodes['n1'] = n1
        self.graph.nodes['n2'] = n2

        self.graph.add_edge(self.edge_id, source=n1.id, target=n2.id)
        assert self.graph.edges
        assert isinstance(self.graph.edges[self.edge_id], Edge)
        assert self.graph.edges[self.edge_id].source == n1
        assert self.graph.edges[self.edge_id].target == n2
