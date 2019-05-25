"""
decoders.py
-----------

Convert GraphData to multiple formats.

"""

def decode_edgelist(graph, out, delimiter=' ', data=False, close=True, return_text=False, write=False):
    text = ''
    for ((node1, node2), *attrs) in graph.edges:
        text += '{}{}{}'.format(
            graph.nodes[node1][0], delimiter, graph.nodes[node2][0])
        if data:
            text += delimiter + delimiter.join([str(d) for d in attrs])
        text += '\n'
    return text


def write(text, out, close=True):
    file = open(out) if isinstance(out, str) else out
    file.write(text)
    if close:
        file.close()
