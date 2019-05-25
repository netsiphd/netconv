"""
test_write.py
-------------

Test output functions.

"""

from sys import stdout
from netconv import GraphData


def test_edgelist():
    """The distance between two equal graphs must be zero."""
    graph = GraphData()
    graph.nodes = [('a',), ('b',), ('c',)]
    graph.edges = [((0, 1), 1), ((1, 2), 2), ((2, 0), 1)]

    with_data = 'a b 1\nb c 2\nc a 1\n'
    assert with_data == graph.write_edgelist(None, return_text=True, data=True)

    no_data = 'a b\nb c\nc a\n'
    assert no_data == graph.write_edgelist(None, return_text=True, data=False)
