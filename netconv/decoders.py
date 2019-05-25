"""
decoders.py
-----------

Convert texts to GraphData.

"""


from .graph import GraphData


def decode_edgelist(text, delimiter=' '):
    """Return a GraphData object converted from a text of edgelist."""
    graph = GraphData()
    n_counter = 0
    label2id = dict()

    for line in text.strip.split('\n'):
        nodes = line.strip().split(sep=delimiter)

        # Add nodes
        for n in nodes:
            if n not in label2id:
                label2id[n] = n_counter
                n_counter += 1
                graph.nodes.append(n)

        # Add the edge
        e = (tuple(label2id[n] for n in nodes),)
        graph.edges.append(e)

    return graph
