class Token:
    def __init__(self, token_type: str, value):
        self._value = value
        self._token_type = token_type

    @property
    def token_type(self):
        return self.token_type

    @property
    def value(self):
        return self._value

    def __repr__(self):
        return self.token_type+" "+self.value


class Integer(Token):
    def __init__(self, value: int):
        super().__init__("INT", value)

    def __repr__(self):
        return "INTEGER "+str(self.value)


class Float(Token):
    def __init__(self, value: float):
        super().__init__("FLOAT", value)

    def __repr__(self):
        return "FLOAT "+str(self.value)


class Operator(Token):
    def __init__(self, token_type: str, value):
        super().__init__(token_type, value)


class Plus(Operator):
    def __init__(self):
        super().__init__("PLUS", '+')

    def __repr__(self):
        return "OPERATOR PLUS"


class Minus(Operator):
    def __init__(self):
        super().__init__("MINUS", '-')

    def __repr__(self):
        return "OPERATOR MINUS"


class Multiply(Operator):
    def __init__(self):
        super().__init__("MULTIPLY", '*')

    def __repr__(self):
        return "OPERATOR MULTIPLY"


class Divide(Operator):
    def __init__(self):
        super().__init__("DIVIDE", '/')

    def __repr__(self):
        return "OPERATOR DIVIDE"


class LParens(Token):
    def __init__(self):
        super().__init__("LPARENS", '(')

    def __repr__(self):
        return "LEFT PARENTHESIS ("


class RParens(Token):
    def __init__(self):
        super().__init__("RPARENS", ')')

    def __repr__(self):
        return "RIGHT PARENTHESIS )"
