import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type  # 'operator' or 'operand'
        self.value = value  # For operators: 'AND'/'OR', for operands: comparison operator
        self.left = left  # Reference to left child or variable
        self.right = right  # Reference to right child or comparison value

    def __repr__(self):
        if self.type == 'operator':
            return f"({self.left} {self.value} {self.right})"
        elif self.type == 'operand':
            return f"{self.left} {self.value} {self.right}"
        return "Node"

    def print_tree(self, level=0):
        indent = "  " * level
        if self.type == 'operator':
            return f"{indent}Operator: {self.value}\n" + \
                   f"{indent}Left:\n{self.left.print_tree(level + 1)}" + \
                   f"{indent}Right:\n{self.right.print_tree(level + 1)}"
        elif self.type == 'operand':
            return f"{indent}Operand: {self.left} {self.value} {self.right}"
        return f"{indent}Node"


def create_rule(rule_string):
    rule_string = re.sub(r'\s+', ' ', rule_string).strip()
    operators = {'AND': 'AND', 'OR': 'OR'}
    comparison_regex = r'(\w+)\s*([><=]+)\s*([\'"]?\w+[\'"]?)'

    def parse_expression(expression):
        stack = []
        last_pos = 0
        main_operator = None

        for i, char in enumerate(expression):
            if char == '(':
                stack.append('(')
            elif char == ')':
                if not stack:
                    raise ValueError(
                        "Mismatched closing parenthesis at position {}".format(i))
                stack.pop()

            elif expression[i:i + 3] in operators and not stack:
                if main_operator is None:
                    main_operator = expression[i:i + 3]
                else:
                    left_expression = expression[last_pos:i].strip()
                    right_expression = expression[i + 3:].strip()
                    left_node = parse_condition(left_expression)
                    right_node = parse_expression(right_expression)
                    return Node('operator', left=left_node, right=right_node, value=main_operator)
                last_pos = i + 3  

        if last_pos < len(expression):
            return parse_condition(expression[last_pos:].strip())

        if stack:  
            raise ValueError("Mismatched opening parenthesis.")

        raise ValueError("Invalid expression provided.")

    def parse_condition(condition):
        condition = condition.strip()
        if condition.startswith('(') and condition.endswith(')'):
            return parse_expression(condition[1:-1])

        match = re.match(comparison_regex, condition)
        if match:
            variable = match.group(1)
            operator = match.group(2)
            value = match.group(3).strip("'\"")
            return Node('operand', left=variable, right=value, value=operator)

        raise ValueError(f"Invalid condition: {condition}")

    ast = parse_expression(rule_string)
    return ast


def evaluate_ast(ast, data):
    if ast.type == 'operator':
        left_result = evaluate_ast(ast.left, data)
        right_result = evaluate_ast(ast.right, data)
        print(
            f"Evaluating: {ast.value} | Left: {left_result} | Right: {right_result}")

        if ast.value == 'AND':
            return left_result and right_result
        elif ast.value == 'OR':
            return left_result or right_result

    elif ast.type == 'operand':
        variable = ast.left
        operator = ast.value
        comparison_value = ast.right

        if variable not in data:
            raise ValueError(f"Missing variable in data: {variable}")


        if operator == '>':
            result = data[variable] > float(comparison_value)
        elif operator == '<':
            result = data[variable] < float(comparison_value)
        elif operator == '=':
            result = data[variable] == comparison_value
        else:
            raise ValueError(f"Invalid operator: {operator}")

        print(
            f"Evaluating: {variable} {operator} {comparison_value} | Result: {result}")
        return result

    return False


@api_view(['POST'])
def evaluate_rule(request):
    try:
        rule_string = request.data.get('rule')
        data = request.data.get('data')

        if not rule_string or not data:
            return Response({'error': 'Both rule and data must be provided.'}, status=status.HTTP_400_BAD_REQUEST)

        ast = create_rule(rule_string)

        print("AST Structure:\n", ast.print_tree())

        result = evaluate_ast(ast, data)

        return Response({'result': result}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
