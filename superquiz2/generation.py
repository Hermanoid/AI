import random

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


def random_expression(function_symbols, leaves, max_depth, depth=0):
    if depth==max_depth or random.random() < 0.5: return random.choice(leaves)
    return [random.choice(function_symbols)] + [random_expression(function_symbols, leaves, max_depth, depth+1) for _ in range(2)]


# Test stuff

def distinct_expressions(expressions):
    def tupleafy(expression):
        if not isinstance(expression, list): return expression
        return (expression[0], tupleafy(expression[1]), tupleafy(expression[2]))
    return {tupleafy(expression) for expression in expressions}

if __name__=="__main__":
    print("Test 1: All expressions valid")
    random.seed(0)
    function_symbols = ['f', 'g', 'h']
    constant_leaves =  list(range(-2, 3))
    variable_leaves = ['x', 'y', 'i']
    leaves = constant_leaves + variable_leaves
    max_depth = 4

    for _ in range(10000):
        expression = random_expression(function_symbols, leaves, max_depth)
        if not is_valid_expression(expression, function_symbols, leaves):
            print("The following expression is not valid:\n", expression)
            break
    else:
        print("OK")

    print("Test 2: Enough expressions distinct")
    random.seed(42) # It's an exceptional number
    function_symbols = ['f', 'g', 'h']
    leaves = ['x', 'y', 'i'] + list(range(-2, 3))
    max_depth = 4
    expressions = [random_expression(function_symbols, leaves, max_depth)
                for _ in range(10000)]
    distinct = distinct_expressions(expressions)
    print(f"Distinct Expressions: {len(distinct)}/{len(expressions)}")
    print("OK" if len(distinct)>1000 else "FAIL")

    print("Test 3: Depth well-distributed")
    # re-use expressions from previous test.

    depths = [depth(expression) for expression in expressions]
    counts = {v: 0 for v in range(5)}
    for d in depths:
        counts[d] += 1
    print("Depth counts: ", counts)
    print("OK" if all(count>=100 for count in counts.values()) else "FAIL")