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
        return "({} {})".format(str(self.left), str(self.right))

    def desugar(self):
        self.left.desugar()
        self.right.desugar()

    def clone(self):
        return Application(self.left.clone(), self.right.clone())

    def debrujin(self, variables):
        self.left.debrujin(variables)
        self.right.debrujin(variables)

    def reduce(self):
        newleft, left_changed = self.left.reduce()
        if left_changed:
            return (Application(newleft, self.right.clone()), True)
        if isinstance(newleft, Abstraction):
            return (newleft.apply(self.right), True)
        newright, right_changed = self.right.reduce()
        return (Application(newleft, newright), right_changed)

    def alpha(self, n, x):
        return Application(
            self.left.alpha(n, x),
            self.right.alpha(n, x)
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
            return "(\\{} . {})".format(params, str(self.term))
        else:
            return "(\\{} {})".format(str(self.variables), str(self.term))

    def desugar(self):
        self.term.desugar()
        if not isinstance(self.variables, list):
            return
        first = self.variables[0]
        for variable in reversed(self.variables[1:]):
            self.term = Abstraction(variable, self.term)
        self.variables = first

    def clone(self):
        return Abstraction(self.variables.clone(), self.term.clone())

    def debrujin(self, variables):
        sub = (self.variables.inner.name,) + variables
        self.term.debrujin(sub)

    def reduce(self):
        newterm, changed = self.term.reduce()
        return (Abstraction(self.variables.clone(), newterm), changed)

    def apply(self, x):
        return self.term.alpha(0, x)

    def alpha(self, n, x):
        return Abstraction(
            self.variables.clone(),
            self.term.alpha(n + 1, x)
        )
