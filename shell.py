from lexer import *


def run(statement: str):
    lexer: list[Token] | SyntaxErrorException = Lexer(statement).tokenize()
    if not isinstance(lexer, SyntaxErrorException):
        parse: list[Token] | Token = Parser(lexer).parse()
        interpret = Interpreter(parse).interpret()

        print(interpret)


while True:
    statement = input("SnakeScript > ")
    run(statement)
