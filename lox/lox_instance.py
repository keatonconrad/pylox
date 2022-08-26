from token import Token
from exceptions import LoxRuntimeError
from lox_function import LoxFunction


class LoxInstance:
    def __init__(self, klass: "LoxClass", value=None):
        self.klass: "LoxClass" = klass
        self.fields: dict = {}
        self.value = value  # Value for literals

    def get(self, name: Token):
        if name.lexeme in self.fields:
            return self.fields.get(name.lexeme)

        method: LoxFunction = self.klass.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)

        raise LoxRuntimeError(name, f'Undefined property "{name.lexeme}".')

    def set(self, name: Token, value: object) -> None:
        self.fields[name.lexeme] = value

    def __str__(self) -> str:
        return f"<{self.klass.name} instance>"
