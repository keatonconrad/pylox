from lox_callable import LoxCallable
from lox_instance import LoxInstance


class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: dict[str, "LoxFunction"]):
        self.name: str = name
        self.methods: dict[str, "LoxFunction"] = methods

    def arity(self) -> int:
        return 0

    def call(self, interpreter: "Interpreter", arguments: list) -> object:
        instance: LoxInstance = LoxInstance(self)
        return instance

    def find_method(self, name: str):
        if name in self.methods:
            return self.methods.get(name)

    def __str__(self):
        return self.name
