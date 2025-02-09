class LambdaError(Exception):
    pass


class LexicalError(LambdaError):
    def __init__(self, message, debug):
        row, col = debug
        super().__init__(
            "{} [on line {}, column {}]".format(message, row, col)
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


class LambdaSyntaxError(LambdaError):
    def __init__(self, message, token):
        row, col = token.debug
        super().__init__(
            "{} [{} - on line {} column {}]".format(
                message, repr(token), row, col))


class ExpectedDifferentToken(LambdaSyntaxError):
    def __init__(self, token, expected):
        super().__init__(
            "Expected token of type '{}'!".format(repr(expected)),
            token)
