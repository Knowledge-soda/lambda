from tokens import Token


class Application:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "Application({}, {})".format(
            repr(self.left),
            repr(self.right)
        )

    def __str__(self):
        leftstr = str(self.left)
        rightstr = str(self.right)
        if isinstance(self.right, Token):
            if isinstance(self.left, Abstraction):
                return "({}) {}".format(leftstr, rightstr)
            return "{} {}".format(leftstr, rightstr)
        if isinstance(self.left, Token):
            return "{} ({})".format(leftstr, rightstr)
        return "({}) ({})".format(leftstr, rightstr)

    def __eq__(self, other):
        if not isinstance(other, Application):
            return False
        return self.left == other.left and self.right == other.right

    def desugar(self):
        self.left.desugar()
        self.right.desugar()

    def resugar(self):
        self.left.resugar()
        self.right.resugar()

    def clone(self):
        return Application(self.left.clone(), self.right.clone())

    def compile(self, termsbook):
        self.left = self.left.compile(termsbook)
        self.right = self.right.compile(termsbook)
        return self

    def decompile(self, program):
        name = program.search(self)
        if name is None:
            return Application(
                self.left.decompile(program),
                self.right.decompile(program))
        return Token.termname(name, (1, 1))

    def debruijn(self, variables):
        self.left.debruijn(variables)
        self.right.debruijn(variables)

    def bruijn(self, variables, free):
        self.left.bruijn(variables, free)
        self.right.bruijn(variables, free)

    def get_free(self, free):
        self.left.get_free(free)
        self.right.get_free(free)

    def reduce(self):
        newleft, left_changed = self.left.reduce()
        if left_changed:
            return (Application(newleft, self.right.clone()), True)
        if isinstance(newleft, Abstraction):
            return (newleft.apply(self.right), True)
        newright, right_changed = self.right.reduce()
        return (Application(newleft, newright), right_changed)

    def beta(self, n, x):
        return Application(
            self.left.beta(n, x),
            self.right.beta(n, x)
        )

    def cut(self, depth, difference):
        return Application(
            self.left.cut(depth, difference),
            self.right.cut(depth, difference)
        )


class Abstraction:
    def __init__(self, variables, term):
        self.variables = variables
        self.term = term

    def __repr__(self):
        if isinstance(self.variables, list):
            params = ", ".join(
                    variable.inner.name for variable in self.variables)
        else:
            params = self.variables.inner.name
        return "Abstraction({}: {})".format(params, repr(self.term))

    def __str__(self):
        if isinstance(self.variables, list):
            params = " ".join(
                    variable.inner.name for variable in self.variables)
            return "λ{} . {}".format(params, str(self.term))
        else:
            return "λ{} . {}".format(str(self.variables), str(self.term))

    def __eq__(self, other):
        if not isinstance(other, Abstraction):
            return False
        return self.term == other.term

    def desugar(self):
        self.term.desugar()
        if not isinstance(self.variables, list):
            return
        first = self.variables[0]
        for variable in reversed(self.variables[1:]):
            self.term = Abstraction(variable, self.term)
        self.variables = first

    def resugar(self):
        term = self.term
        self.variables = [self.variables]
        while isinstance(term, Abstraction):
            self.variables.append(term.variables)
            term = term.term
        self.term = term
        self.term.resugar()

    def clone(self):
        if isinstance(self.variables, list):
            clone_vars = [var.clone() for var in self.variables]
        else:
            clone_vars = self.variables.clone()
        return Abstraction(clone_vars, self.term.clone())

    def compile(self, termsbook):
        self.term = self.term.compile(termsbook)
        return self

    def decompile(self, program):
        name = program.search(self)
        if name is None:
            return Abstraction(
                self.variables.clone(),
                self.term.decompile(program))
        return Token.termname(name, (1, 1))

    def debruijn(self, variables):
        sub = (self.variables.inner.name,) + variables
        self.term.debruijn(sub)

    def get_free(self, free):
        self.term.get_free(free)

    def bruijn(self, variables, free):
        name = self.variables.inner.name[0]
        newname = self.variables.inner.name
        count = 0
        while newname in variables or newname in free:
            newname = "{}{}".format(name, count)
            count += 1
        self.variables.inner.name = newname
        self.term.bruijn((newname, ) + variables, free)

    def reduce(self):
        newterm, changed = self.term.reduce()
        return (Abstraction(self.variables.clone(), newterm), changed)

    def apply(self, x):
        return self.term.beta(0, x)

    def beta(self, n, x):
        return Abstraction(
            self.variables.clone(),
            self.term.beta(n + 1, x)
        )

    def cut(self, depth, difference):
        return Abstraction(
            self.variables.clone(),
            self.term.cut(depth + 1, difference)
        )


class Assignment:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return "Assignment({} = {})".format(
            repr(self.name),
            repr(self.value)
        )

    def __str__(self):
        return "{} = {}".format(str(self.name), str(self.value))


class Program:
    def __init__(self):
        self.lines = []
        self.terms = {}

    def __repr__(self):
        return "PROGRAM:\n\t{}".format(
            "\n\t".join(repr(line) for line in self.lines))

    def __str__(self):
        return "PROGRAM:\n\t{}".format(
            "\n\t".join(str(line) for line in self.lines))

    def add_line(self, line):
        if isinstance(line, Assignment):
            line.value = line.value.compile(self.terms)
            line.value.desugar()
            line.value.debruijn(())
            self.terms[line.name.inner.name] = line.value
        else:
            line = line.compile(self.terms)
        self.lines.append(line)

    def get_singles(self):
        for line in self.lines:
            if not isinstance(line, Assignment):
                yield line

    def get_last(self):
        if not isinstance(self.lines[-1], Assignment):
            return self.lines[-1]

    def search(self, term):
        for key, item in self.terms.items():
            if term == item:
                return key
        return None
