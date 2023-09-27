import itertools

def roulette_wheel_select(population, fitness, r):
    fitnesses = [fitness(p) for p in population]
    total = sum(fitnesses)
    return next(peep for peep, cum_fness in zip (population, itertools.accumulate(fitnesses)) if cum_fness/total > r)

if __name__=="__main__":
    print("Test 1:")
    population = ['a', 'b']

    def fitness(x):
        return 1 # everyone has the same fitness

    for r in [0, 0.33, 0.49999, 0.51, 0.75, 0.99999]:
        print(roulette_wheel_select(population, fitness, r))
    print()

    print("Test 2:")
    population = [0, 1, 2]

    def fitness(x):
        return x

    for r in [0.001, 0.33, 0.34, 0.5, 0.75, 0.99]:
        print(roulette_wheel_select(population, fitness, r))
    print()