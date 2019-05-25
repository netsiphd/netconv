"""
main.py
-------

Class that all formats get converted to and from.

"""


class GraphData():
    """Class that all formats get converted to and from."""

    def __init__(self):
        self.node_attr = ['label']
        self.nodes = []
        self.edge_attr = ['node1', 'node2']
        self.edges = []
        self.graph_attr = {}
        self._node_id = 0

    def __repr__(self):
        return repr(self.graph_attr) + '\n' \
            + repr(self.node_attr) + '\n' \
            + repr(self.nodes) + '\n' \
            + repr(self.edge_attr) + '\n' \
            + repr(self.edges)
