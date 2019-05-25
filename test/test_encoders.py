"""
test_encoders.py
-------------

Test the encoder functions.

"""

from sys import stdout
from netconv import GraphData, encode


def test_edgelist():
    """Test the encoders.encode_edgelist function."""
    graph = GraphData()
    graph.nodes = [('a',), ('b',), ('c',)]
    graph.edges = [((0, 1), 1), ((1, 2), 2), ((2, 0), 1)]

    with_data = 'a b 1\nb c 2\nc a 1\n'
    assert with_data == encode(graph, 'edgelist', attr=True)

    no_data = 'a b\nb c\nc a\n'
    assert no_data == encode(graph, 'edgelist', attr=False)
