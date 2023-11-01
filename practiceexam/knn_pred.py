

def knn_predict(input, examples, distance, combine, k):
    dist_ex = sorted([(distance(input, ex[0]), ex) for ex in examples])
    selected = dist_ex[:k]
    pos = k
    while pos<len(dist_ex) and selected[-1][0] == dist_ex[pos][0]:
        selected.append(dist_ex[pos])
        pos += 1
    return combine([s[1][1] for s in selected])

if __name__=="__main__":
    examples = [
        ([2], '-'),
        ([3], '-'),
        ([5], '+'),
        ([8], '+'),
        ([9], '+'),
    ]
    import numpy as np

    def euclidean_distance(x, y):
        return np.linalg.norm([x_i-y_i for x_i, y_i in zip(x, y)])

    def majority_element(lst):
        counts = {}
        for item in lst: counts[item] = counts.get(item, 0) + 1
        return max(counts, key=counts.get)
    
    distance = euclidean_distance
    combine = majority_element
    
    for k in range(1, 6, 2):
        print("k =", k)
        print("x", "prediction")
        for x in range(0,10):
            print(x, knn_predict([x], examples, distance, combine, k))
        print()