class LexicalError(Exception):
    def __init__(self, message, debug):
        row, col = debug
        super().__init__(
            "[line: {}, column: {}] {}".format(row, col, message)
        )


class LeadingZeroesError(LexicalError):
    def __init__(self, debug):
        super().__init__(
            "Number contains leading zeroes!", debug
        )


class WrongVariableNameError(LexicalError):
    def __init__(self, char, debug):
        super().__init__(
            "On strict mode variable must start with 'v' not '{}'!"
            .format(char),
            debug
        )


class NoIndexError(LexicalError):
    def __init__(self, debug):
        super().__init__("On strict mode variable must have index", debug)


class UnknownTokenError(LexicalError):
    def __init__(self, char, debug):
        super().__init__(
            "No token starts with '{}'!".format(char),
            debug
         )
