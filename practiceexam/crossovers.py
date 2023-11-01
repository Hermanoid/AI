def num_nodes(tree):
    if not isinstance(tree, list): return 1
    return 1 + \
        (num_nodes(tree[1]) if isinstance(tree[1], list) else 1) + \
        (num_nodes(tree[2]) if isinstance(tree[2], list) else 1)

def num_crossovers(e1, e2):
    return num_nodes(e1) * num_nodes(e2)

