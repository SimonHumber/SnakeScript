from parser import *
from Token import *


class Interpreter:
    def __init__(self, expression):
        self.expression = expression

    def interpret(self, expression=None):
        if expression is None:
            expression = self.expression
        if isinstance(expression, Token):
            return expression.value

        index = 0
        if isinstance(expression[0], list):
            left_node = self.interpret(expression[0])
        else:
            left_node = expression[0].value
        index += 1

        while index < len(expression):
            if isinstance(expression[index], Operator):
                operator = expression[index]
                index += 1
                if isinstance(expression[index], list):
                    right_node = self.interpret(expression[index])
                else:
                    right_node = expression[index].value

                if isinstance(operator, Plus):
                    left_node = self.add(left_node, right_node)
                elif isinstance(operator, Minus):
                    left_node = self.minus(left_node, right_node)
                elif isinstance(operator, Multiply):
                    left_node = self.multiply(left_node, right_node)
                elif isinstance(operator, Divide):
                    left_node = self.divide(left_node, right_node)

                index += 1
        return left_node

    def add(self, left_node, right_node):
        return left_node+right_node

    def minus(self, left_node, right_node):
        return left_node-right_node

    def multiply(self, left_node, right_node):
        return left_node*right_node

    def divide(self, left_node, right_node):
        return left_node/right_node
