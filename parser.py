import tokens
from tokens import Literal, END
from abstract import Application, Abstraction, Assignment, Program
from errors import LambdaSyntaxError, ExpectedDifferentToken


class ParserLL1:
    def __init__(self, it):
        self._gen = self._look_ahead_iterator(it)
        next(self)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._gen)

    def _look_ahead_iterator(self, it):
        self.now = next(it)
        for look_ahead in it:
            self.look_ahead = look_ahead
            yield self.now, look_ahead
            self.now = look_ahead

    def must(self, token_type):
        if (self.now.type != token_type):
            raise ExpectedDifferentToken(self.now, token_type)
        ret = self.now
        next(self)
        return ret


def abstraction(it, sugar):
    it.must(Literal.ABSTRACTOR)
    if it.now.type != tokens.Variable:
        raise ExpectedDifferentToken(it.now, tokens.Variable)
    if sugar:
        variables = []
        while it.now.type == tokens.Variable:
            variables.append(it.now)
            next(it)
    else:
        variables = it.now
        next(it)

    if it.now.type == Literal.DOT:
        next(it)
    elif it.now.type != Literal.OPEN:
        raise ExpectedDifferentToken(it.now, Literal.OPEN)
    body = term(it, sugar)
    return Abstraction(variables, body)


def subterm(it, sugar):
    if it.now.type == Literal.ABSTRACTOR:
        return abstraction(it, sugar)
    if it.now.type in (tokens.Variable, tokens.Termname):
        ret = it.now
        next(it)
        return ret
    if it.now.type == Literal.OPEN:
        next(it)
        ret = term(it, sugar)
        it.must(Literal.CLOSED)
        return ret
    raise LambdaSyntaxError("Unknown token at the beggining of subterm",
                            it.now)


def term(it, sugar=True):
    left = subterm(it, sugar)
    while it.now.type in (Literal.ABSTRACTOR, Literal.OPEN,
                          tokens.Variable, tokens.Termname):
        right = subterm(it, sugar)
        left = Application(left, right)
    return left


def assignment(it, sugar):
    termname = it.must(tokens.Termname)
    it.must(Literal.EQUAL)
    value = term(it, sugar)
    return Assignment(termname, value)


def line(it, prog, sugar=True):
    if it.now == Literal.NEWLINE:
        return
    if it.look_ahead.type == Literal.EQUAL:
        prog.add_line(assignment(it, sugar))
    else:
        prog.add_line(term(it, sugar))


def program(it, sugar=True):
    prog = Program()
    while True:
        line(it, prog, sugar)
        if it.now.type == END:
            return prog
        it.must(Literal.NEWLINE)
