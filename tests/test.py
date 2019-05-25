"""Test the GraphData class."""


from graphdata import GraphData


def test_from_edgelist(delimiter=' '):
    # Create example data file
    filename = '../data/example_edgelist.txt'
    el = [('a', 'b'), ('b', 'c'), ('c', 'a')]
    with open(filename, 'w') as _file:
        for e in el:
            _file.write(delimiter.join(e) + '\n')

    # Output example data
    print('Example data')
    print('------------')
    for e in el:
        print(delimiter.join(e))
    print()

    # Read from the data
    gd = GraphData.from_edgelist(filename, delimiter)

    # Output members in GraphData
    print('GraphData object')
    print('----------------')
    print(f'node_attr: {gd.node_attr}')
    print(f'nodes: {gd.nodes}')
    print(f'edge_attr: {gd.edge_attr}')
    print(f'edges: {gd.edges}')
    print(f'graph_attr: {gd.graph_attr}')

    return


if __name__ == '__main__':
    test_from_edgelist()
