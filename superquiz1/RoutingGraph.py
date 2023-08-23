from search import *
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

if __name__ == "__main__":
    map_str = """\
    +-------+
    |  9  XG|
    |X XXX P|
    | S  0FG|
    |XX P XX|
    +-------+
    """

    graph = RoutingGraph(map_str)

    print("Starting nodes:", sorted(graph.starting_nodes()))
    print("Outgoing arcs (available actions) at starting states:")
    for s in sorted(graph.starting_nodes()):
        print(s)
        for arc in graph.outgoing_arcs(s):
            print ("  " + str(arc))

    node = (1,1,5)
    print("\nIs {} goal?".format(node), graph.is_goal(node))
    print("Outgoing arcs (available actions) at {}:".format(node))
    for arc in graph.outgoing_arcs(node):
        print ("  " + str(arc))

    node = (1,7,2)
    print("\nIs {} goal?".format(node), graph.is_goal(node))
    print("Outgoing arcs (available actions) at {}:".format(node))
    for arc in graph.outgoing_arcs(node):
        print ("  " + str(arc))

    node = (3, 7, 0)
    print("\nIs {} goal?".format(node), graph.is_goal(node))

    node = (3, 7, math.inf)
    print("\nIs {} goal?".format(node), graph.is_goal(node))

    node = (3, 6, 5)
    print("\nIs {} goal?".format(node), graph.is_goal(node))
    print("Outgoing arcs (available actions) at {}:".format(node))
    for arc in graph.outgoing_arcs(node):
        print ("  " + str(arc))

    node = (3, 6, 9)
    print("\nIs {} goal?".format(node), graph.is_goal(node))
    print("Outgoing arcs (available actions) at {}:".format(node))
    for arc in graph.outgoing_arcs(node):
        print ("  " + str(arc))

    node = (2, 7, 4)  # at a location with a portal
    print("\nOutgoing arcs (available actions) at {}:".format(node))
    for arc in graph.outgoing_arcs(node):
        print ("  " + str(arc))