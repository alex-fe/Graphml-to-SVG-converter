import os
from unittest.mock import patch

import pytest

from app import Graph
from element import Node


class TestGraph:

    def setup(self):
        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'Test_files', 'test.graphml'
        )
        self.graph = Graph(path)
        self.node_id = 'Test Id'

    @patch('xml.dom.minidom.parse', return_value=None)
    def test_output_path(self, parse):
        path = 'test/path/file.graphml'
        g = Graph(path)
        assert g.svg_path == path.replace('.graphml', '.svg')

        output_path = 'another/path/to/file.svg'
        g = Graph(path, output_path)
        assert g.svg_path == output_path

    def test_add_node(self):
        assert not self.graph.nodes
        self.graph.add_node(self.node_id)
        assert self.graph.nodes
        assert isinstance(self.graph.nodes[self.node_id], Node)

    @pytest.mark.skip()
    def test_get_attrs(self):
        node = self.graph.nodes[self.node_id]
        attribute = 'data'
        assert node.getElementsByTagName(attribute)
        assert self.graph.get_attrs(node, attribute)

        attribute = 'not in node'
        assert not node.getElementsByTagName(attribute)
        assert not self.graph.get_attrs(node, attribute)

    @pytest.mark.skip()
    def test_node_text(self):
        pass
