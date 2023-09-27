import itertools

def n_queens_neighbours(state: tuple[int, int]):
    return sorted(state[:s[0]] + (state[s[1]],) + state[s[0]+1: s[1]] + (state[s[0]],) + state[s[1]+1:] for s in itertools.combinations(range(len(state)), 2))

def n_queens_cost(state):
    """
    Cost = number of conflicts = number of unordered pairs of queens (objects) that threaten/attack each other.
    """
    return sum(abs(q1[0]-q2[0])==abs(q1[1]-q2[1]) for q1, q2 in itertools.combinations(enumerate(state), 2))

def test_neighbours():
    print(n_queens_neighbours((1, 2)))
    print()
    print(n_queens_neighbours((1, 3, 2)))
    print()
    print(n_queens_neighbours((1, 2, 3, 4, 5, 6, 7, 8)))

def test_costs():
    print(n_queens_cost((1, 2)))
    print()
    print(n_queens_cost((1, 3, 2)))
    print()
    print(n_queens_cost((1, 2, 3)))
    print()
    print(n_queens_cost((1,)))
    print()
    print(n_queens_cost((1, 2, 3, 4, 5, 6, 7, 8)))
    print()
    print(n_queens_cost((2, 3, 1, 4)))
    print()
    

if __name__=="__main__":
    test_costs()