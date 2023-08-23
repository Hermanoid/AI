from typing import List
from search import *
import heapq
from math import sqrt


class LocationGraph(Graph):
    def __init__(self, location, radius, starting_nodes, goal_nodes):
        self.location = location
        self.radius = radius
        self._starting_nodes = starting_nodes
        self.goal_nodes = goal_nodes
    
    def starting_nodes(self):
        return self._starting_nodes
    
    def is_goal(self, node):
        return node in self.goal_nodes
    
    def distance(self, node1, node2):
        x1, y1 = node1
        x2, y2 = node2
        return sqrt((x1-x2)**2 + (y1-y2)**2)
    
    def outgoing_arcs(self, tail):
        # for some reason the question requires we sort alphabetically
        # So build all the arcs first and then do the yieldin thing
        tail_loc = self.location[tail]
        arcs = {}
        for key, value in self.location.items():
            if key == tail: continue
            dist = self.distance(tail_loc, value)
            if dist <= self.radius:
                action = f"{tail}->{key}"
                arcs[key] = Arc(tail, key, action=action, cost=dist)
        for arc in sorted(arcs):
            yield arcs[arc]


class LCFSFrontier(Frontier):
    """Implements a frontier container appropriate for depth-first
    search."""

    def __init__(self):
        """The constructor takes no argument. It initialises the
        container to an empty stack."""
        self.container = []
        self.counter = 0

    def add(self, path: List[Arc]):
        heapq.heappush(self.container, (sum([arc.cost for arc in path]), self.counter, path))
        self.counter += 1

    def __iter__(self):
        """The object returns itself because it is implementing a __next__
        method and does not need any additional state for iteration."""
        return self
        
    def __next__(self):
        if len(self.container) > 0:
            return heapq.heappop(self.container)[2]
        else:
            raise StopIteration   # don't change this one
        
def main():
    # graph = LocationGraph(
    #     location={'A': (25, 7),
    #             'B': (1, 7),
    #             'C': (13, 2),
    #             'D': (37, 2)},
    #     radius=15,
    #     starting_nodes=['B'],
    #     goal_nodes={'D'}
    # )

    # solution = next(generic_search(graph, LCFSFrontier()))
    # print_actions(solution)

    graph = ExplicitGraph(nodes=set('ABCD'),
                        edge_list=[('A', 'D', 7), ('A', 'B', 2),
                                    ('B', 'C', 3), ('C', 'D', 1)],
                        starting_nodes=['A'],
                        goal_nodes={'D'})

    solution = next(generic_search(graph, LCFSFrontier()))
    print_actions(solution)

if __name__ == "__main__":
    main()