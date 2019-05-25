"""
decoders.py
-----------

Convert texts to GraphData.

"""


def decode_edgelist(graph, delimiter=' ', attr=False):
    text = ''
    for ((node1, node2), *attrs) in graph.edges:
        text += '{}{}{}'.format(
            graph.nodes[node1][0], delimiter, graph.nodes[node2][0])
        if attr:
            text += delimiter + delimiter.join([str(d) for d in attrs])
        text += '\n'
    return text


def write(text, out, close=True):
    file = open(out) if isinstance(out, str) else out
    file.write(text)
    if close:
        file.close()
