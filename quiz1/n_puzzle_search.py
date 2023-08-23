from typing import List, Literal
from search import *
from collections import deque
import itertools
import copy

BLANK : Literal[' '] = ' '

class SlidingPuzzleGraph(Graph):
    """Objects of this type represent (n squared minus one)-puzzles.
    """

    def __init__(self, starting_state):
        self.starting_state = starting_state

    def outgoing_arcs(self, state: List[List[int | Literal[' ']]]):
        """Given a puzzle state (node) returns a list of arcs. Each arc
        represents a possible action (move) and the resulting state."""
        
        n = len(state) # the size of the puzzle
        
        # Find i and j such that state[i][j] == BLANK
        i, j = 0, 0
        # Oh how I wish for numpy
        for row, col in itertools.product(range(n), range(n)):
            if state[row][col] == BLANK:
                i, j = row, col
                break
        
        def move_action(name_format, move_row, move_col):
            action = name_format.format(state[move_row][move_col])
            new_state = copy.deepcopy(state)
            new_state[i][j], new_state[move_row][move_col] = new_state[move_row][move_col], BLANK
            arcs.append(Arc(state, new_state, action, 1))
        arcs = []
        if i > 0:
            move_action("Move {} down", i-1, j)
        if i < n - 1:
            move_action("Move {} up", i+1, j)
        if j > 0:
            move_action("Move {} right", i, j-1)
        if j < n - 1:
            move_action("Move {} left", i, j+1)
        return arcs

    def starting_nodes(self):
        return [self.starting_state]
    
    def is_goal(self, state):
        """Returns true if the given state is the goal state, False
        otherwise. There is only one goal state in this problem."""
        
        n = len(state)
        for i in range(n):
            for j in range(n):
                current = state[i][j]
                correct = i*n+j
                if correct == 0: correct = BLANK
                if correct != current: return False

        return True
        

class BFSFrontier(Frontier):
    """Implements a frontier container appropriate for depth-first
    search."""

    def __init__(self):
        """The constructor takes no argument. It initialises the
        container to an empty stack."""
        self.container = deque()

    def add(self, path):
        self.container.append(path)

    def __iter__(self):
        """The object returns itself because it is implementing a __next__
        method and does not need any additional state for iteration."""
        return self
        
    def __next__(self):
        if len(self.container) > 0:
            return self.container.popleft()
        else:
            raise StopIteration   # don't change this one

def main():
    graph = SlidingPuzzleGraph([[3,' '],
                            [1, 2]])

    solutions = generic_search(graph, BFSFrontier())
    print_actions(next(solutions))
    # graph = SlidingPuzzleGraph([[1, 2, 5],
    #                         [3, 4, 8],
    #                         [6, 7, ' ']])

    # solutions = generic_search(graph, BFSFrontier())
    # print_actions(next(solutions))


if __name__ == "__main__":
    main()

