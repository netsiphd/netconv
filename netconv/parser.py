"""Parser function to convert graph data file to GraphData object."""


from graph import GraphData


def from_edgelist(filename, delimiter=' '):
    """Return a GraphData object read from an edgelist."""
    gd = GraphData()
    n_counter = 0
    label2id = dict()

    with open(filename, 'r') as _file:
        for line in _file:
            nodes = line.strip().split(sep=delimiter)

            # Add nodes
            for n in nodes:
                if n not in label2id:
                    label2id[n] = n_counter
                    n_counter += 1
                    gd.nodes.append(n)

            # Add the edge
            e = (tuple(label2id[n] for n in nodes),)
            gd.edges.append(e)

        return gd


def main():
    """Empty main funciton."""

    return


if __name__ == '__main__':
    main()
