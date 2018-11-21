from unittest.mock import patch

from app import Graph


class TestGraph:

    def setup(self):
        self.graph = Graph

    @patch('xml.dom.minidom.parse', return_value=None)
    def test_output_path(self, parse):
        path = 'test/path/file.graphml'
        g = Graph(path)
        assert g.svg_path == path.replace('.graphml', '.svg')

        output_path = 'another/path/to/file.svg'
        g = Graph(path, output_path)
        assert g.svg_path == output_path
