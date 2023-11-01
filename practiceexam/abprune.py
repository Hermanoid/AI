from math import inf

pruning_events = []


def search(tree, alpha=-inf, beta=inf, ismin=False):
    global pruning_events
    currbest = inf if ismin else -inf
    for i, item in enumerate(tree):
        newval = None
        if isinstance(item, list):
            newval = search(item, alpha, beta, not ismin)
        else:
            newval=item
        if ismin: 
            if newval < beta: beta = newval
        else:
            if newval > alpha: alpha = newval
        if alpha > beta: 
            # Snip!
            pruning_events.append((alpha, beta))
            del tree[i+1:]
        if ((newval < currbest) if ismin else (newval > currbest)): currbest = newval
    return currbest

if __name__=="__main__":
    # tree = [3, [[2, 1], [4, [7, -2]]], 0]
    tree = [
        [[1, 2], [3, 4], [5, 6]],
        [1, 2, 3],
        [4, 5]
    ]
    print("Result:", search(tree, ismin=False))
    print("Pruning events:", pruning_events)
    print("Pruned tree:", tree)