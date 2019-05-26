"""
decoders.py
-----------

Convert texts to GraphData.

"""

from .graph import GraphData
from io import BytesIO
import lxml.etree as ET

def parse(s):
    try:
        return int(s)
    except (ValueError, TypeError):
        try:
            return float(s)
        except (ValueError, TypeError):
            return s


def decode_edgelist(text, delimiter=' ', attr=False, header=False):
    """Return a GraphData object converted from a text of edgelist."""
    g = GraphData()
    n_counter = 0
    label2id = dict()

    for line in text.strip().split('\n'):
        node1, node2, *attrs = line.strip().split(sep=delimiter)

        # Add nodes
        for n in [node1, node2]:
            if n not in label2id:
                label2id[n] = n_counter
                n_counter += 1
                g.nodes.append((n,))

        # Add the edge
        edge = [(label2id[node1], label2id[node2])]
        if attr:
            edge += attrs
        g.edges.append(tuple(edge))

    return g


def decode_graphml(text):
    """
    Return a GraphData object parsed from `text`.
    """
    G = GraphData()

    it = ET.iterparse(BytesIO(str.encode(text)))
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


def decode_gexf(text):
    """Return a GraphData object converted from the text of a GEXF file."""
    graphdata = GraphData()
    tree = ET.fromstring(text)
    gexf = tree.find('gexf')

    # Obtain the graph attributes
    meta = gexf.find('meta')
    for key, value in meta.items():
        graphdata.graph_attr[key] = value
    for elem in meta.iter():
        if elem.tag != 'meta':
            graphdata.graph_attr[elem.tag] = elem.text

    # Obtain directionality of the graph
    graph = gexf.find('graph')
    directionality = graph.get('defaultedgetype')
    if directionality == 'directed':
        graphdata.graph_attr['directed'] = True
    elif directionality == 'undirected':
        graphdata.graph_attr['directed'] = False
    else:
        graphdata.graph_attr['directed'] = False  # Default to undirected
    # TODO: in theory, individual edges can disobey edgedefault,
    # so we should check the directedness of all edges. However,
    # it is unlikely that many GraphML objects disobey edgedefault
    # in this way.

    # Obtain names of node and edge attributes
    node_attr, edge_attr = ['label'], ['edge']
    node_attr_id2pos, edge_attr_id2pos = dict(), dict()
    node_attr_id2def, edge_attr_id2def = dict(), dict()
    for attrs in graph.findall('attrubutes'):
        is_node_attr = attrs['class'] == 'node'
        attr_names = node_attr if is_node_attr else edge_attr
        id2pos = node_attr_id2pos if is_node_attr else edge_attr_id2pos
        id2default = node_attr_id2def if is_node_attr else edge_attr_id2def
        for attr in attrs.iter('attrubute'):
            attr_names.append(attr['title'])
            id2pos[attr.id] = attr.id + 1  # The 1st attr. is 'label' or 'edge'
            id2default[attr.id] = attr.get('default')

    return graphdata
