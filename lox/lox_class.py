from lox_callable import LoxCallable
from lox_function import LoxFunction
from lox_instance import LoxInstance


class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: dict[str, "LoxFunction"]):
        self.name: str = name
        self.methods: dict[str, "LoxFunction"] = methods

    def arity(self) -> int:
        initializer: LoxFunction = self.find_method("init")
        if not initializer:
            return 0
        return initializer.arity()

    def call(self, interpreter: "Interpreter", arguments: list) -> object:
        instance: LoxInstance = LoxInstance(self)
        initializer: LoxFunction = self.find_method("init")
        if initializer:
            initializer.bind(instance).call(interpreter, arguments)
        return instance

    def find_method(self, name: str):
        return self.methods.get(name)

    def __str__(self):
        return self.name
