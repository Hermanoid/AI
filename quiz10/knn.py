import numpy as np

def euclidean_distance(x, y):
    return np.linalg.norm([x_i-y_i for x_i, y_i in zip(x, y)])

def majority_element(lst):
    counts = {}
    for item in lst: counts[item] = counts.get(item, 0) + 1
    return max(counts, key=counts.get)

def knn_predict(input, examples, distance, combine, k):
    distances = np.array([distance(input, example[0]) for example in examples])
    neighbors = sorted(zip(examples, distances), key=lambda example: example[1])
    selected = neighbors[:k]
    while k < len(neighbors) and selected[-1][1] == neighbors[k][1]:
        selected.append(neighbors[k])
        k += 1
    return combine([s[0][1] for s in selected])

if __name__=="__main__":
    print(euclidean_distance([0, 3, 1, -3, 4.5],[-2.1, 1, 8, 1, 1]))
    print(majority_element([0, 0, 0, 0, 0, 1, 1, 1]))
    print(majority_element("ababc") in "ab")
    print("------")

    examples = [
        ([2], '-'),
        ([3], '-'),
        ([5], '+'),
        ([8], '+'),
        ([9], '+'),
    ]

    distance = euclidean_distance
    combine = majority_element

    for k in range(1, 6, 2):
        print("k =", k)
        print("x", "prediction")
        for x in range(0,10):
            print(x, knn_predict([x], examples, distance, combine, k))
        print()

    print("------")

    examples = [
        ([1], 5),
        ([2], -1),
        ([5], 1),
        ([7], 4),
        ([9], 8),
    ]

    def average(values):
        return sum(values) / len(values)

    distance = euclidean_distance
    combine = average

    for k in range(1, 6, 2):
        print("k =", k)
        print("x", "prediction")
        for x in range(0,10):
            print("{} {:4.2f}".format(x, knn_predict([x], examples, distance, combine, k)))
        print()