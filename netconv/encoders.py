"""
encoders.py
-----------

Convert GraphData to texts.

"""


def encode_edgelist(graph, delimiter=' ', attr=False, header=False):
    text = ''

    if header:
        text += delimiter.join([str(a) for a in graph.edge_attr[:2]])
        if attr:
            text += delimiter
            text += delimiter.join([str(a) for a in graph.edge_attr[2:]])
        text += '\n'

    for ((node1, node2), *attrs) in graph.edges:
        text += '{}{}{}'.format(
            graph.nodes[node1][0], delimiter, graph.nodes[node2][0])
        if attr:
            text += delimiter + delimiter.join([str(d) for d in attrs])
        text += '\n'

    return text

def encode_graphml(graph):
    text = ''
    text += "<?xml version='1.0' encoding='utf-8'?>\n"
    text += '<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n'
    for graph_attr in graph.graph_attr:
        if graph_attr != 'directed':
            text += '<key id="{}" for="graph" attr.name="{}"/>\n'.format(graph_attr, graph_attr) #missing type
    for node_attr in graph.node_attr:
        if node_attr != 'label':
            text += '<key id="{}" for="node" attr.name="{}"/>\n'.format(node_attr, node_attr) #missing type
    for edge_attr in graph.edge_attr:
        if edge_attr != 'edge':
            text += '<key id="{}" for="edge" attr.name="{}"/>\n'.format(edge_attr, edge_attr) #missing type

    if graph.graph_attr.get('directed', False):
        text += '<graph edgedefault="directed">\n'
    else:
        text += '<graph edgedefault="undirected">\n'
        
    for atr, val in graph.graph_attr.items():
        if atr != 'directed' and val is not None:
                text += '<data key="{}">{}</data>\n'.format(atr, val)

    num_node_attrs = len(graph.node_attr)
    for idx, val in enumerate(graph.nodes):
        # not properly escaping
        #TODO: use more concise notation if node has no attrs
        text += '<node id="{}">\n'.format(val[0])
        for ix in range(1, num_node_attrs):
            if val[ix] is not None:
                text += '<data key="{}">{}</data>\n'.format(graph.node_attr[ix], val[ix])
        text += "</node>\n"

    num_edge_attrs = len(graph.edge_attr)
    #TODO: support hyperedges
    for idx, val in enumerate(graph.edges):
        text += '<edge source="{}" target="{}">\n'.format(graph.nodes[val[0][0]][0],
                                                          graph.nodes[val[0][1]][0])
        for ix in range(1, num_edge_attrs):
            if val[ix] is not None:
                text += '<data key="{}">{}</data>\n'.format(graph.edge_attr[ix], val[ix])
        text += "</edge>\n"

    text += '</graph>\n'
    text += '</graphml>\n'

    text = text.replace('&', '&amp;')
    return text


def write(text, out, close=True):
    file = open(out) if isinstance(out, str) else out
    file.write(text)
    if close:
        file.close()
