import collections
import os
import sys
from xml.dom import minidom

# import click
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


class Graph(object):

    def __init__(self, path):
        self.path = path
        self.xml = minidom.parse(self.path)
        self.nodes = {}
        # self.graph = nx.MultiDiGraph()
        # self.node_attrs = {
        #     'pos': {},
        #     'node_color': [],
        #     'alpha': [],
        #     'linewidths': [],
        #     'edgecolor': []
        # }
        # self.node_label_attrs = {
        #     'font_size': [],
        #     'font_color': [],
        #     'font_family': [],
        #     'labels': {},
        # }
        # self.edge_attrs = {
        #     'width': [],
        #     'edge_color': [],
        #     'style': []
        # }

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
                Attribute('Border', **border),
            )
        import pdb; pdb.set_trace()


    def parse_edges(self):
        edges = self.xml.getElementsByTagName('edge')
        for edge in edges:
            line_style = self.get_items(edge, 'y:LineStyle')
            self.edge_attrs['width'] = line_style['width']
            self.edge_attrs['edge_color'] = line_style['color']
            self.edge_attrs['style'] = line_style['type']

            self.graph.add_edge(
                edge.attributes['source'].value,
                edge.attributes['target'].value,
            )

    def export(self):
        nx.draw_networkx_nodes(self.graph, **self.node_attrs)
        nx.draw_networkx_labels(self.graph, **self.node_label_attrs)
        nx.draw_networkx_edges(self.graph, **self.edge_attrs)
        plt.show(self.graph)
        # path.replace('.graphml', '.svg')
        # plt.savefig(path, format='svg')


if __name__ == '__main__':
    path = get_path("/Users/alexfeldman/CS/Freelance/Graphml_converter/Test_files/test.graphml")
    g = Graph(path)
    g.parse_nodes()
    # g.parse_edges()
    # g.export()
