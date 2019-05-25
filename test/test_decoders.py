"""
test_decoders.py
----------------

Test the decoder functions.

"""


from netconv import decode


def test_edgelist(delimiter=' '):
    """Test the decoders.decode_edgelist function."""
    # Create test data
    data_text = 'a b\nb c\nc a\n'

    # Obtain data repr
    data_repr = repr({}) + '\n'
    data_repr += repr(['label']) + '\n'
    data_repr += repr([('a',), ('b',), ('c',)]) + '\n'
    data_repr += repr(['node1', 'node2']) + '\n'
    data_repr += repr([((0, 1),), ((1, 2),), ((2, 0),)])

    # Decode the data text
    graph = decode(data_text, 'edgelist', delimiter)
    assert repr(graph) == data_repr


def test_graphml():
    """Test the decoders.decode_graphml function."""
    # Load test data
    with open('../data/test_data_graphml.graphml', 'r') as _file:
        data_text = _file.read()

    # Obtain data repr
    data_repr = repr({'directed': False}) + '\n'
    data_repr += repr(['label']) + '\n'
    data_repr += repr([('a',), ('b',), ('c',)]) + '\n'
    data_repr += repr(['edge']) + '\n'
    data_repr += repr([((0, 1),), ((1, 2),), ((2, 0),)])

    # Decode the data text
    graph = decode(data_text, 'graphml')
    assert repr(graph) == data_repr
