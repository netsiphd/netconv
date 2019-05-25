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

    def __repr__(self):
        return repr(self.graph_attr) + '\n' \
            + repr(self.node_attr) + '\n' \
            + repr(self.nodes) + '\n' \
            + repr(self.edge_attr) + '\n' \
            + repr(self.edges)

    def write_edgelist(self, out, delimiter=' ', data=False, close=True, return_text=False, write=False):
        text = ''
        for ((node1, node2), *attrs) in self.edges:
            text += '{}{}{}'.format(
                self.nodes[node1][0], delimiter, self.nodes[node2][0])
            if data:
                text += delimiter + delimiter.join([str(d) for d in attrs])
            text += '\n'
        if write:
            self._write(text, out, close)
        if return_text:
            return text

    def _write(self, text, out, close=True):
        file = open(out) if isinstance(out, str) else out
        file.write(text)
        if close:
            file.close()
