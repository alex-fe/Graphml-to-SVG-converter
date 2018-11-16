import os
import sys
from xml.dom import minidom

# import click
import matplotlib.pyplot as plt
import networkx as nx

# from node import Attribute, Edge, Node


# @click.command()
# @click.option('-p', '--path', help='Number of greetings.')
def get_path(path):
    if path is None:
        path = input("Please enter path to Graphml file: ").strip()
    if not os.path.isfile(path) or os.path.splitext(path)[1] != '.graphml':
        sys.exit('Incorrect path')
    return path


class Grapher(object):

    def __init__(self, path):
        self.path = path
        self.xml = minidom.parse(self.path)
        self.graph = nx.MultiDiGraph()

    @staticmethod
    def get_items(element, label):
        try:
            items = element.getElementsByTagName(label)[0].attributes.items()
        except IndexError:
            return {}
        else:
            return {k: v for k, v in items}

    def parse_nodes(self):
        nodes = self.xml.getElementsByTagName('node')
        for node in nodes:
            attrs = {
                **self.get_items(node, 'y:Geometry'),
                **self.get_items(node, 'y:Fill'),
                **self.get_items(node, 'y:BorderStyle'),
                **self.get_items(node, 'y:NodeLabel')
            }
            self.graph.add_node(node.attributes['id'].value, **attrs)

    def parse_edges(self):
        edges = self.xml.getElementsByTagName('edge')
        for edge in edges:
            attrs = {
                **self.get_items(edge, 'y:LineStyle'),
            }
            self.graph.add_edge(
                edge.attributes['source'].value,
                edge.attributes['target'].value,
                **attrs
            )
        import pdb; pdb.set_trace()

    def export(self):
        nx.draw_networkx(self.graph)
        plt.show(self.graph)
        # path.replace('.graphml', '.svg')
        # plt.savefig(path, format='svg')


if __name__ == '__main__':
    path = get_path("/Users/alexfeldman/CS/Freelance/Graphml_converter/Test_files/test.graphml")
    g = Grapher(path)
    g.parse_nodes()
    g.parse_edges()
    # g.export()
