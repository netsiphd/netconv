"""
decoders.py
-----------

Convert texts to GraphData.

"""


from .graph import GraphData
from io import StringIO
import lxml


def decode_edgelist(text, delimiter=' '):
    """Return a GraphData object converted from a text of edgelist."""
    g = GraphData()
    n_counter = 0
    label2id = dict()

    for line in text.strip().split('\n'):
        nodes = line.strip().split(sep=delimiter)

        # Add nodes
        for n in nodes:
            if n not in label2id:
                label2id[n] = n_counter
                n_counter += 1
                g.nodes.append((n,))

        # Add the edge
        e = (tuple(label2id[n] for n in nodes),)
        g.edges.append(e)

    return g


def decode_graphml(text):
    """
    Return a GraphData object parsed from `text`.
    """

    # iterparse expects a file, not a string
    it = ET.iterparse(StringIO(text))

    # strip the XML namespace to simplify things
    for _, el in it:
        if '}' in el.tag:
            el.tag = el.tag.split('}', 1)[1]
    root = it.root

    graph_attrs = {'directed': False}
    node_attrs = list()
    node_idx_to_id = dict()
    node_idx = 0
    directed = False
    edge_attrs = list()
    edge_idx = 0

    # traverse iterator twice, hitting all the nodes and attrs
    # and then all the edges

    # first pass
    for item in root.iter():
        tag, attrib = item.tag, item.attrib
        if tag == 'graph':
            if item.attrib.get('edgedefault',
                               'undirected').lower() == 'directed':
                graph_attrs['directed'] = True
                # TODO: in theory, individual edges can disobey edgedefault,
                # so we should check the directedness of all edges. However,
                # it is unlikely that many GraphML objects disobey edgedefault
                # in this way.

            data = item.findall("data")
            for dat in data:
                if 'key' in dat.attrib:
                    graph_attrs[dat.attrib['key']] = dat.text
        elif tag == 'node':
            if node_idx == 0:
                node_attrs = ['label']
                data = item.getchildren()
                for dat in data:
                    node_attrs.append(list(dat.attrib.values())[0])
            node_idx_to_id[attrib['id']] = node_idx
            node_idx += 1

            entry = [attrib['id']]
            data = item.getchildren()
            for dat in data:
                try:
                    entry.append(parse(dat.text))
                except:
                    print(data)
                    raise

            G.nodes.append(tuple(entry))

    # second pass
    for item in root.iter():
        tag, attrib = item.tag, item.attrib
        if tag == 'edge':
            if edge_idx == 0:
                edge_attrs = ['edge']
                data = item.getchildren()
                for dat in data:
                    edge_attrs.append(list(dat.attrib.values())[0])
            edge_idx += 1

            entry = [(node_idx_to_id[attrib['source']],
                      node_idx_to_id[attrib['target']])]
            data = item.getchildren()
            for dat in data:
                entry.append(parse(dat.text))

            G.edges.append(tuple(entry))
    G.graph_attr = graph_attrs
    G.node_attr = node_attrs
    G.edge_attr = edge_attrs

    return G
