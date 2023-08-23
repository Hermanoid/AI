from search import Arc, Graph
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

def main():
    graph = LocationGraph(
        location={'SW': (-2, -2),
                'NW': (-2, 2),
                'NE': (2, 2),
                'SE': (2, -2)},
        radius = 5,
        starting_nodes=['NE'],
        goal_nodes={'SW'}
    )

    for arc in graph.outgoing_arcs('NE'):
        print(arc)

    print()

    for arc in graph.outgoing_arcs('NW'):
        print(arc)

    print()

    for arc in graph.outgoing_arcs('SW'):
        print(arc)

    print()


    for arc in graph.outgoing_arcs('SE'):
        print(arc)

if __name__ == "__main__":
    main()