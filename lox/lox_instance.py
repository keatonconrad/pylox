from token import Token
from exceptions import LoxRuntimeError


class LoxInstance:
    def __init__(self, klass: "LoxClass"):
        self.klass: "LoxClass" = klass
        self.fields: dict = {}

    def get(self, name: Token):
        if name.lexeme in self.fields:
            return self.fields.get(name.lexeme)

        raise LoxRuntimeError(name, f'Undefined property "{name.lexeme}".')

    def set(self, name: Token, value: object) -> None:
        self.fields[name.lexeme] = value

    def __str__(self) -> str:
        return self.klass.name + " instance"
