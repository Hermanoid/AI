"""
ExplicitGraph(
    nodes={'S', 'A', 'B', 'G'},
    edge_list=[('A', 'B'), ('S', 'G'), ('S', 'A'), ('B', 'G')],
    starting_nodes = ['S'],
    goal_nodes = {'G'}
)

"""
from queue import SimpleQueue


class ExplicitGraph():
    def __init__(self, nodes, edge_list, starting_nodes, goal_nodes):
        self.nodes = nodes
        self.edge_list =edge_list
        self.starting_nodes = starting_nodes
        self.goal_nodes = goal_nodes

    def get_neighbors(self, node):
        neighbors = []
        for edge in self.edge_list:
            if edge[0] == node:
                neighbors.append(edge[1])
        return neighbors

    def is_goal(self, node):
        return node in self.goal_nodes
    
    def starting_nodes(self):
        return self.starting_nodes

def print_path(op, path):
    print(op+"".join(path))

def generic_search(graph: ExplicitGraph):
    """
    graph: ExplicitGraph
    fringe: Stack or Queue (typically)
    """
    # visited = set()
    fringe = SimpleQueue()
    for node in graph.starting_nodes:
        fringe.put([node])
        print_path("+", [node])
    while not fringe.empty():
        path = fringe.get()
        print_path("-", path)
        if graph.is_goal(path[-1]):
            return path
        neighbors = graph.get_neighbors(path[-1])
        for node in neighbors:
            new_path = path+[node]
            fringe.put(new_path)
            print_path("+", new_path)
    return None


graph = ExplicitGraph(
    nodes={'S', 'A', 'B', 'G'},
    edge_list=[('A', 'B'), ('S', 'A'), ('S', 'G'), ('B', 'G')],
    starting_nodes=['S'],
    goal_nodes={'G'})

path = generic_search(graph)
print_path("--> ", path)
