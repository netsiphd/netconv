"""
main.py
-------

Class that all formats get converted to and from.

"""

from .encoders import encode_edgelist

class GraphData():
    """Class that all formats get converted to and from."""

    encoders = {'edgelist': encode_edgelist}
    decoders = {}

    def __init__(self):
        self.node_attr = ['label']
        self.nodes = []
        self.edge_attr = ['edge']
        self.edges = []
        self.graph_attr = {}
        self._node_id = 0

    def __repr__(self):
        return repr(self.graph_attr) + '\n' \
            + repr(self.node_attr) + '\n' \
            + repr(self.nodes) + '\n' \
            + repr(self.edge_attr) + '\n' \
            + repr(self.edges)


def encode(graph, fmt, *args, **kwargs):
    return GraphData.encoders[fmt](graph, *args, **kwargs)


def write(graph, fmt, filename, *args, **kwargs):
    text = encode(graph, fmt, *args, **kwargs)
    with open(filename, 'w') as file:
        file.write(text)


def decode(text, fmt, *args, **kwargs):
    return GraphData.decoders[fmt](text, *args, **kwargs)


def read(filename, fmt, *args, **kwargs):
    with open(filename) as file:
        text = file.read()
    return decode(text, fmt, *args, **kwargs)
