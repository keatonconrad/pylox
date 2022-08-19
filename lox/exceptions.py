from token import Token
from token_type import TokenType


class LoxException(Exception):
    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}")

    def what(self):
        pass


class LoxScannerError(LoxException):
    def __init__(self, line: int, message: str):
        self.line = line
        self.message = message

    def what(self) -> None:
        return self.report(self.line, "", self.message)


class LoxParseError(LoxException):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message

    def what(self) -> None:
        if self.token.type == TokenType.EOF:
            self.report(self.token.line, " at end", self.message)
        else:
            self.report(
                self.token.line, " at '{}'".format(self.token.lexeme), self.message
            )


class LoxRuntimeError(LoxException):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message

    def what(self) -> None:
        if self.token.type == TokenType.EOF:
            self.report(self.token.line, " at end", self.message)
        else:
            self.report(
                self.token.line, " at '{}'".format(self.token.lexeme), self.message
            )


class LoxBreakException(LoxException):
    def __init__(self):
        pass


class LoxReturnException(RuntimeError):
    def __init__(self, value):
        self.value = value


class LoxStaticError(LoxScannerError):
    pass
