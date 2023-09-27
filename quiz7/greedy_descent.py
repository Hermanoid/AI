import random
import itertools

def n_queens_neighbours(state: tuple[int, int]):
    return sorted(state[:s[0]] + (state[s[1]],) + state[s[0]+1: s[1]] + (state[s[0]],) + state[s[1]+1:] for s in itertools.combinations(range(len(state)), 2))

def n_queens_cost(state):
    """
    Cost = number of conflicts = number of unordered pairs of queens (objects) that threaten/attack each other.
    """
    return sum(abs(q1[0]-q2[0])==abs(q1[1]-q2[1]) for q1, q2 in itertools.combinations(enumerate(state), 2))

def greedy_descent(initial_state, neighbours, cost):
    prev_cost = cost(initial_state)
    path = [initial_state]
    curr_state = initial_state
    while True:
        neighborhood = neighbours(curr_state)
        if not neighborhood:
            return path
        costs = [cost(state) for state in neighborhood]
        new_cost = min(costs)
        if new_cost >= prev_cost:
            return path
        curr_state = neighborhood[costs.index(new_cost)] # Yes I know it iterates through the list twice, bite me
        path.append(curr_state)
        prev_cost = new_cost

def greedy_descent_with_random_restart(random_state, neighbours, cost):
    while True:
        state = random_state()
        path = greedy_descent(state, neighbours, cost)
        for s in path: print(s)
        if cost(path[-1]) == 0: return path
        print("RESTART")

def test_greedy_descent():
    def cost(x):
        return x**2

    def neighbours(x):
        return [x - 1, x + 1]

    print("Test 1:")
    for state in greedy_descent(4, neighbours, cost):
        print(state)
    print()
    print("Test 2:")
    for state in greedy_descent(-6.75, neighbours, cost):
        print(state)
    print()

    def cost(x):
        return -x**2

    def neighbours(x):
        return [x - 1, x + 1] if abs(x) < 5 else []

    print("Sneaky little test I failed")
    for state in greedy_descent(0, neighbours, cost):
        print(state)

def test_greedy_random_restart():
    N = 6
    random.seed(0)

    def random_state():
        return tuple(random.sample(range(1,N+1), N))   

    print("Test 1:")
    greedy_descent_with_random_restart(random_state, n_queens_neighbours, n_queens_cost)
    print()

    N = 8
    random.seed(0)

    print("Test 2:")
    greedy_descent_with_random_restart(random_state, n_queens_neighbours, n_queens_cost)
    print()

if __name__=="__main__":
    test_greedy_random_restart()