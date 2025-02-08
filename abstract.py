class Application:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return "Application({}, {})".format(
                repr(self.left),
                repr(self.right)
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
