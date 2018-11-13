import os
import sys
from xml.dom import minidom

import click
import matplotlib.pyplot as plt
import networkx as nx

from node import Border, Fill, Geometry, Label, Node


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
        self.nodes = []

    @staticmethod
    def get_items(element, label):
        return element.getElementsByTagName(label)[0].attributes.items()

    def parse_nodes(self):
        nodes = self.xml.getElementsByTagName('node')
        for node in nodes:
            id_ = node.attributes['id'].value
            geometry = Geometry(*self.get_items(node, 'y:Geometry'))
            fill = Fill(*self.get_items(node, 'y:Fill'))
            border = Border(*self.get_items(node, 'y:BorderStyle'))
            label = Border(*self.get_items(node, 'y:NodeLabel'))
            nn = Node(id_, label, geometry, fill, border)
            self.nodes.append(nn)

    def export(graph, path):
        nx.draw_networkx(graph)
        plt.show(graph)
        path.replace('.graphml', '.svg')
    # plt.savefig(path, format='svg')


if __name__ == '__main__':
    path = get_path("/Users/alexfeldman/Desktop/test.graphml")
    g = Grapher(path)
    g.parse_nodes()
    # export(graph, path)
