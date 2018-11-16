import os
import sys
from xml.dom import minidom

import click
import matplotlib.pyplot as plt
import networkx as nx

from node import Attribute, Edge, Node


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
        self.nodes = {}
        self.edges = []

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
            id_ = node.attributes['id'].value
            geometry = Attribute(**self.get_items(node, 'y:Geometry'))
            fill = Attribute(**self.get_items(node, 'y:Fill'))
            border = Attribute(**self.get_items(node, 'y:BorderStyle'))
            label = Attribute(**self.get_items(node, 'y:NodeLabel'))
            self.nodes[id_] = Node(id_, label, geometry, fill, border)
        import pdb; pdb.set_trace()

    def parse_edges(self):
        edges = self.xml.getElementsByTagName('edges')
        for edge in edges:
            ed = Edge(
                edge.attributes['id'].value,
                edge.attributes['source'].value,
                edge.attributes['target'].value,
                Attribute(*self.get_items(edge, 'y:LineStyle')),
            )
            self.edges.append(ed)

    def export(graph, path):
        nx.draw_networkx(graph)
        plt.show(graph)
        path.replace('.graphml', '.svg')
    # plt.savefig(path, format='svg')


if __name__ == '__main__':
    path = get_path("/Users/alexfeldman/CS/Freelance/Graphml_converter/Test_files/test.graphml")
    g = Grapher(path)
    g.parse_nodes()
    # g.parse_edges()
    # export(graph, path)
