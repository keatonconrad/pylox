from lox_callable import LoxCallable
from lox_instance import LoxInstance


class LoxClass(LoxCallable):
    def __init__(self, name: str):
        self.name: str = name

    def arity(self) -> int:
        return 0

    def call(self, interpreter: "Interpreter", arguments: list) -> object:
        instance: LoxInstance = LoxInstance(self)
        return instance

    def __str__(self):
        return self.name
