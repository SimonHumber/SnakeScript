from lexer import *
from Token import *


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
