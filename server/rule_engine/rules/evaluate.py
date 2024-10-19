def evaluate_ast(ast, data):
    if ast['type'] == 'operand':
        return eval(f"{data[ast['left']]} {ast['operator']} {ast['right']}")
    elif ast['type'] == 'operator':
        left_result = evaluate_ast(ast['left'], data)
        right_result = evaluate_ast(ast['right'], data)
        if ast['value'] == 'AND':
            return left_result and right_result
        elif ast['value'] == 'OR':
            return left_result or right_result
    return False
