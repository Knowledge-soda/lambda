from errors import (
    LeadingZeroesError,
    WrongVariableNameError,
    NoIndexError,
    UnknownTokenError
)
from tokens import Token, END


class LookAheadText:
    def __init__(self, text):
        self._gen = self._look_ahead_iterator(iter(text))
        self.row = 1
        self.col = 1

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._gen)

    def _look_ahead_iterator(self, it):
        self.now = next(it)
        for look_ahead in it:
            self.look_ahead = look_ahead
            yield self.now, look_ahead
            if self.now == '\n':
                self.row += 1
                self.col = 1
            else:
                self.col += 1
            self.now = look_ahead
        self.look_ahead = END
        yield self.now, self.look_ahead

    def get_debug(self):
        return self.row, self.col

    def read_number(self):
        if self.now == "0":
            if self.look_ahead != END and self.look_ahead.isdecimal():
                raise LeadingZeroesError(self.get_debug())
            return "0"
        buffer = [self.now]
        while self.look_ahead != END and self.look_ahead.isdecimal():
            next(self)
            buffer.append(self.now)
        return "".join(buffer)

    def read_termname(self):
        buffer = [self.now]
        while self.look_ahead != END and self.look_ahead.isalnum():
            next(self)
            buffer.append(self.now)
        return "".join(buffer)


def tokenize(text, strict=False):
    it = LookAheadText(text)
    depth = 0
    for cur, new in it:
        debug = it.get_debug()
        if new == END:
            twochar = cur
        else:
            twochar = "".join((cur, new))
            try:
                literal = Token.literal(twochar, debug)
                next(it)
                yield literal
                continue
            except ValueError:
                pass
        try:
            if cur == "\\":
                cur = "λ"
            literal = Token.literal(cur, debug)
            if cur == "(":
                depth += 1
            if cur == ")":
                depth -= 1
            if cur != "\n" or not depth:
                yield literal
            continue
        except ValueError:
            pass
        if cur.isspace():
            continue
        if cur.islower():
            if strict and cur != "v":
                raise WrongVariableNameError(cur, debug)
            if new == END or not new.isdecimal():
                if strict:
                    raise NoIndexError(debug)
                else:
                    yield Token.variable(cur, debug)
                    continue
            next(it)
            yield Token.variable(cur + it.read_number(), debug)
        elif cur.isupper():
            yield Token.termname(it.read_termname(), debug)
        else:
            raise UnknownTokenError(twochar, debug)
    yield Token(END, it.get_debug())
    yield Token(END, it.get_debug())
