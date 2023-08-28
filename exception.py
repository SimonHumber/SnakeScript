class Exception:
    def __init__(self):
        pass


class SyntaxErrorException(Exception):
    def __init__(self, statement: str):
        print(statement)
        for i in range(len(statement)-1):
            print(" ", end="")
        print("^")
        print("SyntaxErrorException")
