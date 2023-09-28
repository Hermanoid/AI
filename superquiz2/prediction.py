import random
import operator
import itertools
import time
from copy import copy
import pandas as pd


def is_valid_expression(object, function_symbols, leaf_symbols):
    return (
        isinstance(object, int)
        or object in leaf_symbols
        or (
            isinstance(object, list)
            and len(object) == 3
            and object[0] in function_symbols
            and is_valid_expression(object[1], function_symbols, leaf_symbols)
            and is_valid_expression(object[2], function_symbols, leaf_symbols)
        )
    )


def depth(expression):
    if not isinstance(expression, list):
        return 0
    return max(depth(expression[1]), depth(expression[2])) + 1


def evaluate(expression, bindings):
    if isinstance(expression, int):
        return expression
    if isinstance(expression, str):
        return bindings[expression]
    return bindings[expression[0]](evaluate(expression[1], bindings), evaluate(expression[2], bindings))


def evaluate_default(expression, bindings):
    return evaluate(expression, bindings | {"+": operator.add, "-": operator.sub, "*": operator.mul})


def random_expression(function_symbols, leaves, max_depth, depth=0):
    if depth == max_depth or random.random() < 0.5:
        return random.choice(leaves)
    return [random.choice(function_symbols)] + [random_expression(function_symbols, leaves, max_depth, depth + 1) for _ in range(2)]


class Symbols:
    def __init__(self, funcs: list, leaf_vars: list, max_const: int):
        self.funcs = funcs
        self.leaf_vars = leaf_vars
        self.leaf_consts = list(range(-max_const, max_const + 1))
        self.max_const = max_const


# Recursive Generator! Ahhh!!
# In retrospect I can see that this is just an overcomplicated, generator-based version of a BFS search. Oops.
def systematic_expression_recursive(syms: Symbols, depth):
    # Start with vars, constants
    if depth == 0:
        for atom in itertools.chain(syms.leaf_vars, syms.leaf_consts):
            yield atom
    elif depth == 1:
        # Start with +/- (with strictly positive constants on the right)
        for func, left, right in itertools.product(
            ["+", "-"], syms.leaf_vars, itertools.chain(syms.leaf_vars, range(1, syms.max_const + 1))
        ):
            if left == right:
                continue
            yield [func, left, right]
        # Then * (excluding 0 and 1 but including negative numbers on the right)
        for left, right in itertools.product(
            syms.leaf_vars, itertools.chain(syms.leaf_vars, range(-syms.max_const, 0), range(2, syms.max_const + 1))
        ):
            yield ["*", left, right]
    else:
        # For depth>0 expressions, use some intelligence. Skip expressions:
        #  - of only constants (ex: 1-2)
        #  - that are reorderings of the same expression (ex: 1+2, 2+1)
        #  - that involve restatements of the same constant op (ex: x+1, x- (-1))
        #  - that are redundant/don't add to an expression (x*0, x+0, x-x, x*1)
        # To do this:
        #  - enforce some left/right order (variable left, variable or constant left)
        #  - Since we have +/- ops, we can get away with only using non-negative constants
        #  - Since zero is always redundant (x*0 could just be the constant 0, x+0 just x), can use only strictly positive constants
        # This is going to involve hardcoding functions. Alas.
        # Some rough testing showed this reduced the number of depth-1 expressions from 200 to 50 (such nice, even numbers!)
        # ... and depth 2 from 7500-ish (with depth-1-only filtering) to 6395 (unimpressive, actually)
        # ... and depth 3 from 169117742 (this was even with filtering on depth-1 expressions) to 120935795 (a 28% reduction, that's something I guess)
        strictly_positive = list(range(1, syms.max_const + 1))
        right_atoms = {
            "+": syms.leaf_vars + strictly_positive,
            "-": syms.leaf_vars + strictly_positive,
            "*": syms.leaf_vars + list(range(-syms.max_const, 0)) + list(range(2, syms.max_const + 1)),
        }
        # If depth=1, we want to use to the same fill logic, but never fill right or left
        # This is funky but I promise the code is more compact this way
        fill_vals = ((False,), (False,)) if depth == 1 else ((False, True), (False, True))
        for func, fill_left, fill_right in itertools.product(["+", "-", "*"], *fill_vals):
            left_gen = systematic_expression_recursive(syms, depth - 1) if fill_left else syms.leaf_vars
            right_gen = systematic_expression_recursive(syms, depth - 1) if fill_right else right_atoms[func]
            for left, right in itertools.product(left_gen, right_gen):
                if func == "-" and left == right:
                    continue
                yield [func, left, right]


def systematic_expression(syms: Symbols, max_depth):
    for depth in range(max_depth + 1):
        for expr in systematic_expression_recursive(syms, depth):
            yield expr


def generate_rest(initial_sequence, expression, length_to_generate):
    if length_to_generate == 0:
        return []
    sequence = copy(initial_sequence)
    starting_i = len(initial_sequence)
    for i in range(starting_i, starting_i + length_to_generate):
        sequence.append(evaluate_default(expression, {"x": sequence[i - 2], "y": sequence[i - 1], "i": i}))
    return sequence[-length_to_generate:]


def predict_rest(sequence, method="systematic", limit=500000):
    syms = Symbols(["+", "-", "*"], ["x", "y", "i"], 5)
    max_depth = 3
    initial_seq = sequence[:2]
    rest = sequence[2:]
    to_gen = len(sequence) - 2
    generator = {
        "random": (random_expression(syms.funcs, syms.leaf_vars + syms.leaf_consts, max_depth) for _ in range(limit)),
        "systematic": systematic_expression(syms, max_depth),
    }[method]
    for guess_expr, _ in zip(generator, range(limit)):  # zip is used to limit the number of guesses
        guess_rest = generate_rest(initial_seq, guess_expr, to_gen)
        if guess_rest == rest:
            print("Found expression: ", guess_expr)
            return generate_rest(sequence, guess_expr, 5)
    print("Failed to find an expression!")
    return[]


def test_gen_rest():
    print("Test 1:")
    initial_sequence = [0, 1, 2]
    expression = "i"
    length_to_generate = 5
    print(generate_rest(initial_sequence, expression, length_to_generate))

    print("Test 2:")
    # no particular pattern, just an example expression
    initial_sequence = [-1, 1, 367]
    expression = "i"
    length_to_generate = 4
    print(generate_rest(initial_sequence, expression, length_to_generate))

    print("Test 3:")
    initial_sequence = [4, 6, 8, 10]
    expression = ["*", ["+", "i", 2], 2]
    length_to_generate = 5
    print(generate_rest(initial_sequence, expression, length_to_generate))

    print("Test 4:")
    initial_sequence = [4, 6, 8, 10]
    expression = ["+", 2, "y"]
    length_to_generate = 5
    print(generate_rest(initial_sequence, expression, length_to_generate))

    print("Test 5:")
    initial_sequence = [0, 1]
    expression = "x"
    length_to_generate = 6
    print(generate_rest(initial_sequence, expression, length_to_generate))

    print("Test 6 (fib):")
    # Fibonacci sequence
    initial_sequence = [0, 1]
    expression = ["+", "x", "y"]
    length_to_generate = 5
    print(generate_rest(initial_sequence, expression, length_to_generate))

    print("Test 7:")
    initial_sequence = [367, 367, 367]
    expression = "y"
    length_to_generate = 5
    print(generate_rest(initial_sequence, expression, length_to_generate))

    print("Test 8:")
    # no pattern, just a demo
    initial_sequence = [0, 1, 2]
    expression = -1
    length_to_generate = 5
    print(generate_rest(initial_sequence, expression, length_to_generate))

    print("Test 9:")
    initial_sequence = [0, 1, 2]
    expression = "i"
    length_to_generate = 0
    print(generate_rest(initial_sequence, expression, length_to_generate))


def test_pred_rest():
    random.seed(0)

    def test_seq(ctr, seq, method):
        print(f"Test {ctr}: ", seq)
        start = time.perf_counter()
        the_rest = predict_rest(seq, method)
        end = time.perf_counter()
        delta = (end-start)
        print(f"{delta:.6f}s: {the_rest}")
        print()
        return delta

    def test_batch(batch: list[list[int]], methods):
        times = []
        for method in methods:
            method_times = []
            print("*** Using Method:", method)
            for i, seq in enumerate(batch):
                delta = test_seq(i, seq, method)
                method_times.append(delta)
            print()
            times.append(method_times)
        print("Times:")
        df = pd.DataFrame(zip(*times, (t[1]/t[0] for t in zip(*times))), columns=methods+["ratio"])
        print(df)
        

    test_batch(
        [
            [0, 1, 2, 3, 4, 5, 6, 7],
            [0, 2, 4, 6, 8, 10, 12, 14],
            [31, 29, 27, 25, 23, 21],
            [0, 1, 4, 9, 16, 25, 36, 49],
            [3, 2, 3, 6, 11, 18, 27, 38],
            [0, 1, 1, 2, 3, 5, 8, 13],
            [0, -1, 1, 0, 1, -1, 2, -1],
            [1, 3, -5, 13, -31, 75, -181, 437],
        ], ["random", "systematic"]
    )

    # Some fun ones from OEIS:
    # print("Motzkin numbers: ", predict_rest([1, 1, 2, 4, 9, 21, 51, 127]))
    # print("Bell numbers: ", predict_rest([1, 1, 2, 5, 15, 52, 203, 877]))
    # print("Catalan numbers: ", predict_rest([1, 1, 2, 5, 14, 42, 132, 429]))
    # Those didn't work....

def test_pred_fun_stuff():
    print("Tests! ")
    print("Hard seq 1: ", predict_rest([15, 29, 56, 108, 208])) # a(n) = 2 * a(n-1) - 2^i I think
    print("Hard seq 2: ", predict_rest([13, -21, 34, 55, 89]))
    
    # My  boi isn't managing those hard ones very well, lets try medium
    print("Medium test 1", predict_rest([-2, 5, -4, 3, -6])) # a(n) = a(n-2) - 2, I think
    print("Medium test 3", predict_rest([75, 15, 25, 5, 15])) # divide by 5, add 10... interested to see how this it... it doesn't!
    print("Medium test 4", predict_rest([1, 2, 6, 24, 120])) # Factorials! Script should find y*i (actually y+y*i, that's funny... must be i+1)
    print("Medium test 5", predict_rest([183, 305, 527, 749 ,961])) # Add 222... no way can this thing find it... nope
    print("Medium test 6", predict_rest([16, 22, 34, 58, 106])) # I got y + 3*2^(i+1)), this model can't find exp but 2(y-5) works, woah)\
    print("Medium test 7", predict_rest([17, 40, 61, 80, 97])) # y + (25-2i) but that's horrible... it finds (y-x)+(y-2), very neat encoding of that i expression
    print("Medium test 8", predict_rest([55, 34, 21, 13, 8])) # Backwards fibonacci, easy dub
    print("Medium test 9", predict_rest([259, 131, 67, 35, 19])) # I got decreasing powers of 2 + 3, it will prolly get (x-y)+3... nope, just fails (ohh it would need a divide-by-2 op)



if __name__ == "__main__":
    test_pred_rest()
    