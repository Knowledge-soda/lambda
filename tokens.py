from enum import Enum

from errors import UndefinedTerm


class END:
    pass


class Literal(Enum):
    ABSTRACTOR = "λ"
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

    def __str__(self):
        return self.name

    def clone(self):
        return Variable(self.name)


class Termname:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "TERMNAME '{}'".format(self.name)

    def __str__(self):
        return self.name


class Token:
    def __init__(self, inner, debug, index=None):
        self.inner = inner
        self.debug = debug
        self.index = index
        if isinstance(self.inner, Literal) or self.inner == END:
            self.type = self.inner
        else:
            self.type = type(self.inner)

    def __repr__(self):
        if self.index is not None and self.index != -1:
            return "VARIABLE '{}'".format(self.index)
        return repr(self.inner)

    def __str__(self):
        return str(self.inner)

    @classmethod
    def literal(cls, char, debug):
        return cls(Literal(char), debug)

    @classmethod
    def variable(cls, name, debug):
        return cls(Variable(name), debug)

    @classmethod
    def termname(cls, name, debug):
        return cls(Termname(name), debug)

    def desugar(self):
        pass

    def resugar(self):
        pass

    def clone(self):
        if self.type != Variable:
            raise RuntimeError
        return Token(self.inner.clone(), self.debug, self.index)

    def compile(self, termsbook):
        if self.type == Variable:
            return self
        trans = termsbook.get(self.inner.name, None)
        if trans is None:
            raise UndefinedTerm(self.inner.name, self.debug)
        return trans.clone()

    def debrujin(self, variables):
        if self.type != Variable:
            raise RuntimeError
        if self.inner.name in variables:
            self.index = variables.index(self.inner.name)
        else:
            self.index = -1

    def get_free(self, free):
        if self.index == -1:
            free.add(self.inner.name)

    def brujin(self, variables, free):
        if self.index >= 0:
            self.inner.name = variables[self.index]

    def reduce(self):
        return (self.clone(), False)

    def beta(self, n, x):
        if self.index > n:
            return Token(self.inner.clone(), self.debug, self.index - 1)
        elif n == self.index:
            return x.cut(0, n)
        else:
            return self.clone()

    def cut(self, depth, difference):
        if self.type != Variable:
            raise RuntimeError
        new_index = self.index
        if new_index >= depth:
            new_index += difference
        return Token(self.inner.clone(), self.debug, new_index)
