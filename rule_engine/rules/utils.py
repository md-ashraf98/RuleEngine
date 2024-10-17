# rule_engine/utils.py
import ast
import re
from .models import Node

def create_rule(rule_string):
    def parse_condition(condition):
        condition = condition.strip()

        stack = []
        current_condition = []
        i = 0

        while i < len(condition):
            char = condition[i]

            if char == '(':
                stack.append(''.join(current_condition).strip())
                current_condition = []
            elif char == ')':
                if current_condition:
                    completed_condition = ''.join(current_condition).strip()
                    if completed_condition:
                        stack.append(completed_condition)
                    current_condition = []

                if stack:
                    last_condition = stack.pop()
                    if last_condition:
                        current_condition.append(last_condition)
            elif condition[i:i+3] in ['AND', 'OR']:
                operator = condition[i:i+3]
                current_condition.append(operator)
                i += 2
            else:
                current_condition.append(char)

            i += 1

        if current_condition:
            completed_condition = ''.join(current_condition).strip()
            if completed_condition:
                stack.append(completed_condition)

        if not stack:
            raise ValueError("Invalid condition format")

        root = None
        for part in stack:
            if 'AND' in part or 'OR' in part:
                operator = 'AND' if 'AND' in part else 'OR'
                left, right = part.split(f' {operator} ', 1)
                left_node = parse_condition(left.strip())
                right_node = parse_condition(right.strip())
                root = Node.objects.create(type='operator', value=operator, left=left_node, right=right_node)
            else:
                root = Node.objects.create(type='operand', value=part.strip())

        return root

    return parse_condition(rule_string)


def evaluate_rule(node, data):
    if node.type == "operand":
        try:
            attr, op, val = re.split(r'\s*(>=|<=|>|<|=|!=)\s*', node.value)
            val = int(val.strip("'")) if val.isdigit() else val.strip("'")
            if attr not in data:
                raise ValueError(f"Attribute '{attr}' not found in data.")

            if op == ">":
                return data[attr] > val
            elif op == "<":
                return data[attr] < val
            elif op == "=":
                return data[attr] == val
            elif op == "!=":
                return data[attr] != val
            elif op == ">=":
                return data[attr] >= val
            elif op == "<=":
                return data[attr] <= val
            else:
                raise ValueError(f"Invalid operator '{op}' in rule.")
        except Exception as e:
            return f"Error: {str(e)}"
    elif node.type == "operator":
        left_result = evaluate_rule(node.left, data)
        right_result = evaluate_rule(node.right, data)

        if node.value == "AND":
            return left_result and right_result
        elif node.value == "OR":
            return left_result or right_result
    return False


def combine_rules(rules):
    root = None
    for rule in rules:
        node = create_rule(rule)
        if root is None:
            root = node
        else:
            root = Node.objects.create(type='operator', value='OR', left=root, right=node)
    return root
