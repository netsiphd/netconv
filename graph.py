"""
main.py
-------

Class that all formats get converted to and from.

"""

class GraphData():
    """Class that all formats get converted to and from."""

    def __init__(self):
        self.node_attr = ['id']
        self.nodes = []
        self.edge_attr = ['edge']
        self.edges = []
        self.graph_attr = {}
        self._node_id = 0

    def write_edgelist(self, out, delimiter=' ', data=False, close=True):
        text = ''
        for ((node1, node2), *data) in self.edges:
            text += '{}{}{}'.format(
                self.nodes[node1][0], delimiter, self.nodes[node2][0])
            if data:
                text += delimiter + delimiter.join([str(d) for d in data])
            text += '\n'
        self._write(text, out, close)

    def _write(self, text, out, close=True):
        file = open(out) if isinstance(out, str) else out
        file.write(text)
        if close:
            file.close()
