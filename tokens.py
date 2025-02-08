from enum import Enum


class END:
    pass


class Literal(Enum):
    ABSTRACTOR = "\\"
    OPEN = "("
    CLOSED = ")"
    DOT = "."
    EQUAL = "="
    NEWLINE = "\n"


class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "VARIABLE '{}'".format(self.name)


class Termname:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "TERMNAME '{}'".format(self.name)


class Token:
    def __init__(self, inner, debug):
        self.inner = inner
        self.debug = debug
        if isinstance(self.inner, Literal):
            self.type = self.inner
        else:
            self.type = type(self.inner)

    def __repr__(self):
        return repr(self.inner)

    @classmethod
    def literal(cls, char, debug):
        return cls(Literal(char), debug)

    @classmethod
    def variable(cls, name, debug):
        return cls(Variable(name), debug)

    @classmethod
    def termname(cls, name, debug):
        return cls(Termname(name), debug)
