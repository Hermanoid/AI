from typing import List
from search import *
import heapq
import math

MOVE_COST = 5
PORTAL_COST = 10
FUEL_UP_COST = 15
MAX_FUEL = 9
FUEL = "F"
PORTAL = "P"
GOAL = "G"
SOLAR_AGENT = "S"
WALLS = {"X", "|", "-", "+"}
DIRECTIONS = [('N' , -1, 0),
            ('E' ,  0, 1),
            ('S' ,  1, 0),
            ('W' ,  0, -1),]

class RoutingGraph(Graph):
    def __init__(self, map_str: str):
        """
        Parses a map of the form:
        +--------+
        |  G    G|
        |  XXX  P|
        |  S X F |
        |    X 2 |
        +--------+
        Where:
        - S is a solar agent (infinite fuel)
        - G is a goal (customer)
        - X is a wall
        - 2 is an agent with only 2 units remaining fuel
        - F is a fuel station
        - P is a portal (teleports to any other portal)
        """
        self.map_str = map_str.strip()
        self._starting_nodes = []
        self.special_coords = {
            FUEL: set(),
            PORTAL: set(),
            GOAL: set(),
        }
        self.map_arr = self.map_str.splitlines()
        self.map_arr = [line.strip() for line in self.map_arr]
        for row, line in enumerate(self.map_arr):
            for col, char in enumerate(line):
                if char == SOLAR_AGENT:
                    # Solar lads have infinite fuel
                    self._starting_nodes.append((row, col, math.inf))
                elif char.isdigit():
                    self._starting_nodes.append((row, col, int(char)))
                elif char in self.special_coords:
                    self.special_coords[char].add((row, col))

    def starting_nodes(self):
        return self._starting_nodes
    
    def is_goal(self, node):
        row, col, fuel = node
        return (row, col) in self.special_coords[GOAL]
    
    def manhattan_distance(self, n1, n2):
        return abs(n1[0] - n2[0]) + abs(n1[1] - n2[1])

    def estimated_cost_to_goal(self, node):
        dist =  min(self.manhattan_distance(node, goal) for goal in self.special_coords[GOAL])
        return dist * MOVE_COST
    
    def outgoing_arcs(self, tail):
        # for some reason the question requires we sort alphabetically
        # So build all the arcs first and then do the yieldin thing
        row, col, fuel = tail
        arcs = []
        
        curr_char =  self.map_arr[row][col]
        for direction, row_delta, col_delta in DIRECTIONS:
            new_row, new_col = row + row_delta, col + col_delta
            if self.map_arr[new_row][new_col] not in WALLS and fuel > 0:
                arcs.append(Arc(tail, (new_row, new_col, fuel-1), action=direction, cost=MOVE_COST))
        if curr_char == FUEL and fuel < MAX_FUEL:
            arcs.append(Arc(tail, (row, col, MAX_FUEL), action='Fuel up', cost=FUEL_UP_COST))
        elif curr_char == PORTAL:
            for portal_coord in sorted(self.special_coords[PORTAL].difference({(row, col)})):
                portal_row, portal_col = portal_coord
                arcs.append(Arc(tail, (portal_row, portal_col, fuel), action=f"Teleport to ({portal_row}, {portal_col})", cost=PORTAL_COST))

        return arcs


class AStarFrontier(Frontier):
    """Implements a frontier container appropriate for depth-first
    search."""

    def __init__(self, graph: RoutingGraph):
        """The constructor takes no argument. It initialises the
        container to an empty stack."""
        self.container = []
        self.counter = 0
        self.graph = graph
        self.visited = set()

    def add(self, path: List[Arc]):
        cost = sum(arc.cost for arc in path)
        heuristic = self.graph.estimated_cost_to_goal(path[-1].head)
        heapq.heappush(self.container, (cost + heuristic, self.counter, path))
        self.counter += 1

    def __iter__(self):
        """The object returns itself because it is implementing a __next__
        method and does not need any additional state for iteration."""
        return self
        
    def __next__(self):
        while len(self.container) > 0:
            path = heapq.heappop(self.container)[2]
            if path[-1].head not in self.visited:
                self.visited.add(path[-1].head)
                return path
        raise StopIteration   # don't change this one

def print_map(map_graph: RoutingGraph, frontier: AStarFrontier, solution: List[Arc]):
    # Convert the map_str into a 2D array, then fill in visited and solution locations with "." and "*"
    # Then print it out
    map_arr = [list(line) for line in map_graph.map_arr]
    if solution:
        # Skip the first head so we don't overwrite the starting node
        for arc in solution:
            row, col, _ = arc.head
            # Don't overwrite anything interesting
            if map_arr[row][col] ==" ":
                map_arr[row][col] = "*"

    for node in frontier.visited:
        row, col, _ = node
        if map_arr[row][col] ==" ":
            map_arr[row][col] = "."

    for line in map_arr:
        print("".join(line))

        
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

    map_str = """\
    +------------------------------+
    |    X                         |
    |  P XG                P       |
    |    X                 F       |
    |    X F                       |
    |    X                         |
    |    X       F                 |
    |    XXXXX  X        F         |
    |  9      XX                   |
    +------------------------------+
    """

    map_graph = RoutingGraph(map_str)
    frontier = AStarFrontier(map_graph)
    solution = next(generic_search(map_graph, frontier), None)
    print_map(map_graph, frontier, solution)

if __name__ == "__main__":
    main()