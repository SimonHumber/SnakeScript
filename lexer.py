from exception import *
from Token import *

NUMBERS = "0123456789"
OPERATORS = "+-*/"
LPARENS = '('
RPARENS = ')'
CHARS = '_-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
VARIABLE = "var"
QUOTES = '"'
WHITESPACE = " \t\n"

variables = {}


class Lexer:
    def __init__(self, statement: str):
        self.statement: str = statement
        self.idx: int = 0
        self.current_char: str = statement[0]
        self.tokens: list[Token] = []
        self.left_bracket_count = 0

    def advance(self):
        self.idx += 1

        if self.idx < len(self.statement):
            self.current_char = self.statement[self.idx]

    def tokenize(self) -> list[Token] | SyntaxErrorException:
        while self.idx < len(self.statement):
            if self.current_char in NUMBERS:
                self.tokens.append(self.num_analyze())
            elif self.current_char in OPERATORS:
                self.tokens.append(self.op_analyze())
                self.advance()
            elif self.current_char in CHARS:
                variable = self.keyword_analyzer()
                if isinstance(variable, SyntaxErrorException):
                    return variable
                else:
                    self.tokens.append(variable)
            elif self.current_char == LPARENS:
                self.left_bracket_count += 1
                self.tokens.append(LParens())
                self.advance()
            elif self.current_char == RPARENS:
                if self.left_bracket_count == 0:
                    return SyntaxErrorException(self.statement[:self.idx+1])
                else:
                    self.left_bracket_count -= 1
                    self.tokens.append(RParens())
                    self.advance()
            elif self.current_char in WHITESPACE:
                self.advance()
            else:
                return SyntaxErrorException(self.statement[:self.idx+1])
        if self.left_bracket_count > 0:
            return SyntaxErrorException(self.statement+" ")
        return self.tokens

    def num_analyze(self) -> Token:
        number: str = self.current_char
        isFloat: bool = False
        self.advance()
        while self.idx < len(self.statement):
            if self.current_char in NUMBERS:
                number += self.current_char
                self.advance()
            elif self.current_char == "." and not isFloat:
                isFloat = True
                number += self.current_char
                self.advance()
            else:
                break
        if isFloat:
            return Float(float(number))
        else:
            return Integer(int(number))

    def op_analyze(self) -> Token:
        operator = self.current_char
        if operator == '+':
            token = Plus()
        elif operator == '-':
            token = Minus()
        elif operator == '*':
            token = Multiply()
        else:
            token = Divide()
        # TODO make exception if operator at end of statement or following char is syntax error
        return token

    def keyword_analyzer(self):
        string = ""
        while True:
            if self.current_char in WHITESPACE or self.idx >= len(self.statement):
                break
            elif self.current_char in CHARS+"_-":
                string += self.current_char
                self.advance()
            else:
                return SyntaxErrorException(self.statement[:self.idx+1])
        if string == VARIABLE:
            if self.current_char in WHITESPACE:
                self.advance()
                return self.var_analyzer()
            else:
                return SyntaxErrorException(self.statement[:self.idx+1])
        elif string in variables:
            token = variables[string]
            return token[0]
        else:
            return SyntaxErrorException(self.statement[:self.idx+1])

    def var_analyzer(self):
        name = ""
        while True:
            if self.idx >= len(self.statement):
                return SyntaxErrorException(self.statement[:self.idx+1])
            elif self.current_char in WHITESPACE:
                self.advance()
            elif self.current_char in CHARS:
                name += self.current_char
                self.advance()
            elif self.current_char in NUMBERS and len(name) > 0:
                name += self.current_char
                self.advance()
            elif self.current_char == '=' and len(name) > 0:
                self.advance()
                # fix issue so we can assign variable to a variable
                assignment_tokens = self.tokenize()
                if isinstance(assignment_tokens, list):
                    assignment = Interpreter(
                        Parser(assignment_tokens).parse()).interpret()
                    token = Lexer(str(assignment)).tokenize()
                    variables[name] = token
                    return token
                elif isinstance(assignment_tokens, SyntaxErrorException):
                    return assignment_tokens
                else:
                    SyntaxErrorException(self.statement[:self.idx+1])
            else:
                return SyntaxErrorException(self.statement[:self.idx+1])


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


class Parser:
    def __init__(self, statement: list[Token]):
        self.tokens: list[Token] = statement
        self.idx: int = 0
        self.current_token: Token = self.tokens[0]
        self.left_parens_counter = 0

    def advance(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.current_token = self.tokens[self.idx]

    def parse(self):
        return self.expression()

    def factor(self):
        if isinstance(self.current_token, Integer) or isinstance(self.current_token, Float):
            return self.current_token
        elif isinstance(self.current_token, LParens):
            self.advance()
            expression = self.expression()
            return expression
        else:
            print("error")
            exit()

    def term(self):
        output = self.factor()
        self.advance()
        while isinstance(self.current_token, Multiply) or isinstance(self.current_token, Divide):
            operator = self.current_token
            self.advance()
            if isinstance(self.current_token, RParens):
                output = [output, operator, self.current_token]
            else:
                right_node = self.factor()
                output = [output, operator, right_node]
            self.advance()
        return output

    def expression(self):
        output = self.term()
        while isinstance(self.current_token, Plus) or isinstance(self.current_token, Minus):
            operator = self.current_token
            self.advance()
            if isinstance(self.current_token, RParens):
                output = [output, operator, self.current_token]
            else:
                right_node = self.term()
                output = [output, operator, right_node]
        return output
