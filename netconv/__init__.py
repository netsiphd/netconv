# -*- coding: utf-8 -*-
"""
netconv is a lightweight graph format converter.

Authors:  Chia-Hung Yang <yang.chi@husky.neu.edu>
          Leonardo Torres <leo@leotrs.com>
          Stefan McCabe <mccabe.s@husky.neu.edu>
          Jean-Gabriel Young <jgyou@umich.edu>
"""
from .graph import GraphData
from .decoders import decode_edgelist
from .encoders import encode_edgelist


DECODERS = {'edgelist': decode_edgelist}
ENCODERS = {'edgelist': encode_edgelist}


def decode(text, fmt, *args, **kwargs):
    return DECODERS[fmt](text, *args, **kwargs)


def encode(graph, fmt, *args, **kwargs):
    return ENCODERS[fmt](graph, *args, **kwargs)


def read(filename, fmt, *args, **kwargs):
    with open(filename) as file:
        text = file.read()
    return decode(text, fmt, *args, **kwargs)


def write(graph, fmt, filename, *args, **kwargs):
    text = encode(graph, fmt, *args, **kwargs)
    with open(filename, 'w') as file:
        file.write(text)


__all__ = ['GraphData', 'read', 'write']


__authors__ = ["Chia-Hung Yang <yang.chi@husky.neu.edu>",
               "Leonardo Torres <leo@leotrs.com>",
               "Stefan McCabe <mccabe.s@husky.neu.edu>",
               "Jean-Gabriel Young <jgyou@umich.edu>"]
__license__ = "MIT"
__name__ = 'netconv'
__date__ = "May 26th, 2019"
__version__ = '0.0.1'
__contact__ = 'leo@leotrs.com'
__desc__ = 'Lightweight graph format converter.'
