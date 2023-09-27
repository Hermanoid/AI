
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


def test_valid_expression():
    print("Test 1")
    function_symbols = ['f', '+']
    leaf_symbols = ['x', 'y']
    expression = 1

    print(is_valid_expression(expression, function_symbols, leaf_symbols))
    print()

    print("Test 2")
    function_symbols = ['f', '+']
    leaf_symbols = ['x', 'y']
    expression = 'y'

    print(is_valid_expression(
            expression, function_symbols, leaf_symbols))
    print()

    print("Test 3")
    function_symbols = ['f', '+']
    leaf_symbols = ['x', 'y']
    expression = 2.0

    print(is_valid_expression(
            expression, function_symbols, leaf_symbols))
    print()

    print("Test 4")
    function_symbols = ['f', '+']
    leaf_symbols = ['x', 'y']
    expression = ['f', 123, 'x']

    print(is_valid_expression(
            expression, function_symbols, leaf_symbols))
    print()

    print("Test 5")
    function_symbols = ['f', '+']
    leaf_symbols = ['x', 'y']
    expression = ['f', ['+', 0, -1], ['f', 1, 'x']]

    print(is_valid_expression(
            expression, function_symbols, leaf_symbols))
    print()

    print("Test 6")
    function_symbols = ['f', '+']
    leaf_symbols = ['x', 'y']
    expression = ['+', ['f', 1, 'x'], -1]

    print(is_valid_expression(
            expression, function_symbols, leaf_symbols))
    print()

    print("Test 7")
    function_symbols = ['f', '+']
    leaf_symbols = ['x', 'y', -1, 0, 1]
    expression = ['f', 0, ['f', 0, ['f', 0, ['f', 0, 'x']]]]

    print(is_valid_expression(
            expression, function_symbols, leaf_symbols))
    print()

    print("Test 8")
    function_symbols = ['f', '+']
    leaf_symbols = ['x', 'y']
    expression = 'f'

    print(is_valid_expression(
            expression, function_symbols, leaf_symbols))
    print()

    print("Test 9")
    function_symbols = ['f', '+']
    leaf_symbols = ['x', 'y']
    expression = ['f', 1, 0, -1]

    print(is_valid_expression(
            expression, function_symbols, leaf_symbols))
    print()

    print("Test 10")
    function_symbols = ['f', '+']
    leaf_symbols = ['x', 'y']
    expression = ['x', 0, 1]

    print(is_valid_expression(
            expression, function_symbols, leaf_symbols))
    print()

    print("Test 11")
    function_symbols = ['f', '+']
    leaf_symbols = ['x', 'y']
    expression = ['g', 0, 'y']

    print(is_valid_expression(
            expression, function_symbols, leaf_symbols))
    

def test_depth():
    expression = 12
    print(depth(expression))

    expression = 'weight'
    print(depth(expression))

    expression = ['add', 12, 'x']
    print(depth(expression))

    expression = ['add', ['add', 22, 'y'], 'x']
    print(depth(expression))

if __name__=="__main__":
    test_valid_expression()
    # test_depth()