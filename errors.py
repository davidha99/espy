class CompilerException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "Compile error: %s" % self.message


class CircularList(CompilerException):
    pass


class UndefinedVariable(CompilerException):
    pass


class RedefinedVariable(CompilerException):
    pass


class EspyTypeError(CompilerException):
    # 'TypeError' is a built-in Python exception
    pass


class EspySyntaxError(CompilerException):
    # SyntaxError is also a built-in Python exception
    pass


class EspyArityError(CompilerException):
    pass


class InvalidArgumentNumber(CompilerException):
    pass


class EspyStackOverflow(CompilerException):
    def __init__(self):
        super().__init__("Stack overflown")
