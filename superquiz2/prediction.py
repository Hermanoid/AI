import random
import operator
import itertools

def is_valid_expression(object, function_symbols, leaf_symbols):
    return isinstance(object, int) \
        or object in leaf_symbols \
        or (isinstance(object, list)
            and len(object) == 3
            and object[0] in function_symbols
            and is_valid_expression(object[1], function_symbols, leaf_symbols)
            and is_valid_expression(object[2], function_symbols, leaf_symbols))

def depth(expression):
    if not isinstance(expression, list): return 0
    return max(depth(expression[1]), depth(expression[2])) + 1

def evaluate(expression, bindings):
    if isinstance(expression, int): return expression
    if isinstance(expression, str): return bindings[expression]
    return bindings[expression[0]](evaluate(expression[1], bindings), evaluate(expression[2], bindings))

def evaluate_default(expression, bindings):
    return evaluate(expression, bindings | {"+": operator.add, "-": operator.sub, "*": operator.mul})

def random_expression(function_symbols, leaves, max_depth, depth=0):
    if depth==max_depth or random.random() < 0.5: return random.choice(leaves)
    return [random.choice(function_symbols)] + [random_expression(function_symbols, leaves, max_depth, depth+1) for _ in range(2)]

class Symbols:
    def __init__(self, funcs:list, leaf_vars: list, leaf_consts: list):
        self.funcs = funcs
        self.leaf_vars = leaf_vars
        self.leaf_consts = leaf_consts

def systematic_atom(syms: Symbols):
    for var in syms.leaf_vars: yield var
    for const in syms.leaf_consts: yield const

def systematic_funcs(syms: Symbols, fill_left, fill_right, depth):
    left_gen = systematic_expression_recursive(syms, depth - 1) if fill_left else systematic_atom(syms)
    right_gen = systematic_expression_recursive(syms, depth - 1) if fill_right else systematic_atom(syms)
    for func, left, right in itertools.product(syms.funcs, left_gen, right_gen):
        yield [func, left, right]

# Recursive Generator! Ahhh!!
def systematic_expression_recursive(syms: Symbols, depth):
    # Start with vars, constants
    if depth == 0:
        for atom in systematic_atom(syms): yield atom
    elif depth==1:
        # For level-1 recursion, use some intelligence. Skip expressions:
        #  - of only constants (ex: 1-2)
        #  - that are reorderings of the same expression (ex: 1+2, 2+1)
        #  - that involve restatements of the same constant op (ex: x+1, x- (-1))
        for expr in systematic_funcs(syms, False, False, 0): yield expr
    elif depth==2:
        # Switch to an expression.
        # Start with no recursive expressions, then left, then right, then both
        for fill_left, fill_right in itertools.product((False, True), repeat=2):
            for expr in systematic_funcs(syms, fill_left, fill_right, depth-1): yield expr
    

def systematic_expression(syms: Symbols, max_depth):
    for depth in range(max_depth+1):
        for expr in systematic_expression_recursive(syms, depth):
            yield expr


def generate_rest(initial_sequence, expression, length_to_generate):
    if length_to_generate==0: return []
    sequence = initial_sequence
    starting_i = len(initial_sequence)
    for i in range(starting_i, starting_i+length_to_generate):
        sequence.append(evaluate_default(expression, {"x": sequence[i-2], "y": sequence[i-1], "i": i}))
    return sequence[-length_to_generate:]

def predict_rest(sequence):
    function_symbols = ["+", "-", "*"]
    leaf_symbols = ["x", "y", "i", -2, -1, 0, 1 ,2]
    max_depth = 3
    initial_seq = sequence[:2]
    rest = sequence[2:]
    to_gen = len(sequence) - 2
    for _ in range(1000000):
        guess_expr = random_expression(function_symbols, leaf_symbols, max_depth)
        guess_rest = generate_rest(initial_seq, guess_expr, to_gen)
        if guess_rest == rest:
            print("Found expression: ", guess_expr)
            return generate_rest(sequence, guess_expr, 5)
    raise Exception("Failed to find an expression!")

def test_gen_rest():
    print("Test 1:")
    initial_sequence = [0, 1, 2]
    expression = 'i' 
    length_to_generate = 5
    print(generate_rest(initial_sequence, 
                        expression,
                        length_to_generate))
    
    print("Test 2:")
    # no particular pattern, just an example expression
    initial_sequence = [-1, 1, 367]
    expression = 'i' 
    length_to_generate = 4
    print(generate_rest(initial_sequence,
                        expression,
                        length_to_generate))

    print("Test 3:")
    initial_sequence = [4, 6, 8, 10]
    expression = ['*', ['+', 'i', 2], 2]
    length_to_generate = 5
    print(generate_rest(initial_sequence, 
                        expression, 
                        length_to_generate))

    print("Test 4:")
    initial_sequence = [4, 6, 8, 10]
    expression = ['+', 2, 'y']
    length_to_generate = 5
    print(generate_rest(initial_sequence, 
                        expression, 
                        length_to_generate))

    print("Test 5:")
    initial_sequence = [0, 1]
    expression = 'x'
    length_to_generate = 6
    print(generate_rest(initial_sequence, 
                        expression, 
                        length_to_generate))

    print("Test 6 (fib):")
    # Fibonacci sequence
    initial_sequence = [0, 1]
    expression = ['+', 'x', 'y']
    length_to_generate = 5
    print(generate_rest(initial_sequence, 
                        expression, 
                        length_to_generate))

    print("Test 7:")
    initial_sequence = [367, 367, 367]
    expression = 'y'
    length_to_generate = 5
    print(generate_rest(initial_sequence, 
                        expression, 
                        length_to_generate))

    print("Test 8:")
    # no pattern, just a demo
    initial_sequence = [0, 1, 2]
    expression = -1 
    length_to_generate = 5
    print(generate_rest(initial_sequence, 
                        expression, 
                        length_to_generate))

    print("Test 9:")
    initial_sequence = [0, 1, 2]
    expression = 'i'
    length_to_generate = 0
    print(generate_rest(initial_sequence, 
                        expression, 
                        length_to_generate))
    

def test_pred_rest():
    random.seed(0)
    def test_seq(ctr, seq):
        print(f"Test {ctr}: ", seq)
        the_rest = predict_rest(seq)
        print(the_rest)
        print()
    test_seq(1, [0, 1, 2, 3, 4, 5, 6, 7])
    test_seq(2, [0, 2, 4, 6, 8, 10, 12, 14])
    test_seq(3, [31, 29, 27, 25, 23, 21])
    test_seq(4, [0, 1, 4, 9, 16, 25, 36, 49])
    test_seq(5, [3, 2, 3, 6, 11, 18, 27, 38])
    test_seq(6, [0, 1, 1, 2, 3, 5, 8, 13])
    test_seq(7, [0, -1, 1, 0, 1, -1, 2, -1])
    test_seq(8, [1, 3, -5, 13, -31, 75, -181, 437])

if __name__=="__main__":
    test_pred_rest()