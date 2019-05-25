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

    with_attr = 'a b 1\nb c 2\nc a 1\n'
    assert with_attr == encode(graph, 'edgelist', attr=True)

    no_attr = 'a b\nb c\nc a\n'
    assert no_attr == encode(graph, 'edgelist', attr=False)
