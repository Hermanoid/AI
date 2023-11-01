import numpy as np

# gotta love numpy
def construct_perceptron(weights, bias):
    """Returns a perceptron function using the given paramers."""
    def perceptron(input):
        return int((np.dot(input, weights) + bias) >= 0)
    
    return perceptron # this line is fine

def accuracy(classifier, inputs, expected_outputs):
    """Returns the proportion of the inputs that are correctly classified."""
    return sum(classifier(input) == expected for input, expected in zip(inputs, expected_outputs))/len(inputs)

def learn_perceptron_parameters(weights, bias, training_examples, learn_rate, max_epochs):
    """Returns the weights and bias after training on the given examples."""
    weights = np.array(weights, dtype=np.float32)
    training_examples = [(np.array(inp, dtype=np.float32), example) for inp, example in training_examples]
    for _ in range(max_epochs):
        all_good = True
        for input, expected in training_examples:
            # Skip construction of a perceptron closure (for speeeeed)
            actual = int((np.dot(input, weights) + bias) >= 0)
            if expected==actual: continue
            all_good = False
            weights += learn_rate * (expected - actual) * input
            bias += learn_rate * (expected - actual)
            print("Example", [input, expected], "weights", weights, "bias", bias)
        if all_good: break
    return list(weights), bias

if __name__ == "__main__":
    # weights = [2, -4]
    # bias = 0
    # perceptron = construct_perceptron(weights, bias)

    # print(perceptron([1, 1]))
    # print(perceptron([2, 1]))
    # print(perceptron([3, 1]))
    # print(perceptron([-1, -1]))

    # print("------")

    # perceptron = construct_perceptron([-1, 3], 2)
    # inputs = [[1, -1], [2, 1], [3, 1], [-1, -1]]
    # targets = [0, 1, 1, 0]

    # print(accuracy(perceptron, inputs, targets))

    # print("------")

    # weights = [2, -4]
    # bias = 0
    # learning_rate = 0.5
    # examples = [
    # ((0, 0), 0),
    # ((0, 1), 0),
    # ((1, 0), 0),
    # ((1, 1), 1),
    # ]
    # max_epochs = 50

    # weights, bias = learn_perceptron_parameters(weights, bias, examples, learning_rate, max_epochs)
    # print(f"Weights: {weights}")
    # print(f"Bias: {bias}\n")

    # perceptron = construct_perceptron(weights, bias)

    # print(perceptron((0,0)))
    # print(perceptron((0,1)))
    # print(perceptron((1,0)))
    # print(perceptron((1,1)))
    # print(perceptron((2,2)))
    # print(perceptron((-3,-3)))
    # print(perceptron((3,-1)))

    # print("------")

    # weights = [2, -4]
    # bias = 0
    # learning_rate = 0.5
    # examples = [
    # ((0, 0), 0),
    # ((0, 1), 1),
    # ((1, 0), 1),
    # ((1, 1), 0),
    # ]
    # max_epochs = 50

    # weights, bias = learn_perceptron_parameters(weights, bias, examples, learning_rate, max_epochs)
    # print(f"Weights: {weights}")
    # print(f"Bias: {bias}\n")
    
    weights = [-1, 1]
    bias = 0
    learning_rate = 0.5
    examples = [
        ([-2, 0], 0),    # index 0 (first example)
        ([-1, 1], 0),
        ([1, 1], 0),
        ([2, 0], 1),
        ([1, -1], 1),
        ([-1, -1], 1),
    ]
    weights, bias = learn_perceptron_parameters(weights, bias, examples, learning_rate, 50)