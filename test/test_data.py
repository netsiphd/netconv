"""
test_data.py
------------

Test that decoding and encoding data yields the data intact.

"""

from netconv import decode, encode


def test_edgelist():
    with open('../data/karate.txt') as file:
        text = file.read()
    assert text == encode(decode(text, 'edgelist', attr=True),
                          'edgelist', attr=True)

def test_edgelist_no_attr():
    with open('../data/karate_no_attr.txt') as file:
        text = file.read()
    assert text == encode(decode(text, 'edgelist', attr=False),
                          'edgelist', attr=False)

def test_graphml():
    with open('../data/karate.gml') as file:
        text = file.read()
    assert text == encode(decode(text, 'graphml'), 'graphml')
