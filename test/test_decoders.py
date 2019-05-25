"""
test_decoders.py
----------------

Test the decoder functions.

"""


from netconv import decode


def test_edgelist(delimiter=' '):
    """Test the decoders.decode_edgelist function."""
    # Create test data
    el = [('a', 'b'), ('b', 'c'), ('c', 'a')]
    data = 'a b\nb c\nc a\n'

    # Obtain data repr
    data_repr = repr({}) + '\n'
    data_repr += repr(['label']) + '\n'
    data_repr += repr([('a',), ('b',), ('c',)]) + '\n'
    data_repr += repr(['edge']) + '\n'
    data_repr += repr([(e,) for e in el])

    # Read from the data
    graph = decode(data, 'edgelist', delimiter)
    assert repr(graph) == data_repr