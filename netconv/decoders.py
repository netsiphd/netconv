"""
decoders.py
-----------

Convert texts to GraphData.

"""

from .graph import GraphData
from io import BytesIO
import lxml.etree as ET
from copy import copy


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
    node_attrs = set()
    node_idx_to_id = dict()
    node_idx = 0
    directed = False
    edge_attrs = set()
    edge_idx = 0
    num_edges = 0

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
            data = item.getchildren()
            for dat in data:
                node_attrs.update({list(dat.attrib.values())[0]})

            node_idx_to_id[attrib['id']] = node_idx
            node_idx += 1

            entry = [attrib['id']]
            G.nodes.append(entry)

        elif tag == 'edge':
            num_edges += 1
            data = item.getchildren()
            for dat in data:
                edge_attrs.update({list(dat.attrib.values())[0]})

    edge_attrs = ['edge'] + list(edge_attrs)
    edge_attr_lookup = {v:i for i, v in enumerate(edge_attrs)}
    G.edges = [[None for _ in range(len(edge_attrs))] for _ in range(num_edges)]
    for node in G.nodes:
        node.extend([None for _ in range(len(node_attrs))])
    node_attrs = ['label'] + list(node_attrs)
    node_attr_lookup = {v:i for i, v in enumerate(node_attrs)}
    node_idx = 0

    # second pass
    for item in root.iter():
        tag, attrib = item.tag, item.attrib
        if tag == 'node':
            data = item.getchildren()
            for dat in data:
                idx = node_attr_lookup[dat.attrib.values()[0]]
                G.nodes[node_idx][idx] = parse(dat.text)
            node_idx += 1

        elif tag == 'edge':

            G.edges[edge_idx][0] = (node_idx_to_id[attrib['source']],
                      node_idx_to_id[attrib['target']])

            data = item.getchildren()
            for dat in data:
                idx = edge_attr_lookup[dat.attrib.values()[0]]
                G.edges[edge_idx][idx] = parse(dat.text)

            edge_idx += 1

    G.graph_attr = graph_attrs
    G.node_attr = node_attrs
    G.edge_attr = edge_attrs
    G.edges = [tuple(x) for x in G.edges]
    G.nodes = [tuple(x) for x in G.nodes]

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
    # Handle labeled names of nodes and edges plus weights for edges
    nodes, edges = graph.find('nodes'), graph.find('edges')
    if nodes.find(".//node[@label]") is not None:
        node_attr.append('name')
    if edges.find(".//edge[@label]") is not None:
        edge_attr.append('name')
    if edges.find(".//edge[@weight]") is not None:
        edge_attr.append('weight')
    node_attr_def = [None for _ in node_attr]
    edge_attr_def = [None for _ in edge_attr]

    # Handle additional attributes that are defined under 'graph'
    node_attr_id2pos, edge_attr_id2pos = dict(), dict()
    for attrs in graph.iter('attrubutes'):
        is_node_attr = (attrs.get('class') == 'node')
        attr_names = node_attr if is_node_attr else edge_attr
        id2pos = node_attr_id2pos if is_node_attr else edge_attr_id2pos
        counter = 1
        def_vals = node_attr_def if is_node_attr else edge_attr_def
        for attr in attrs.iter('attrubute'):
            attr_names.append(attr.get('title'))
            id2pos[attr.get('id')] = counter
            counter += 1
            def_vals.append(attr.get('default'))

    graphdata.node_attr = node_attr
    graphdata.edge_attr = edge_attr

    # Obtain the list of nodes and edges, including their attribute values
    node_has_name = 'name' in node_attr
    for node in nodes.iter('node'):
        n_vec = copy(node_attr_def)
        n_vec[0] = node.get('id')  # Identifier of the node
        if node_has_name:
            n_vec[node_attr.index('name')] = node.get('label')
        for attrval in node.iterfind("./attrvalues/attrvalue"):
            n_vec[node_attr_id2pos[attrval.get('for')]] = attrval.get('value')
        graphdata.nodes.append(n_vec)

    edge_has_name, edge_has_weight = 'name' in edge_attr, 'weight' in edge_attr
    for edge in edges.iter('edge'):
        e_vec = copy(edge_attr_def)
        e_vec[0] = (edge.get('source'), edge.get('target'))
        if edge_has_name:
            e_vec[edge_attr.index('name')] = edge.get('label')
        if edge_has_weight:
            e_vec[edge_attr.index('weight')] = edge.get('weight')
        for attrval in edge.iterfind("./attrvalues/attrvalue"):
            e_vec[edge_attr_id2pos[attrval.get('for')]] = attrval.get('value')
        graphdata.edges.append(e_vec)

    # TODO: graph has an optional attribute 'mode' which specifies if the graph
    # is static or dynamical (temporal). This is out of the scope of the
    # project but still worths noting.

    return graphdata
