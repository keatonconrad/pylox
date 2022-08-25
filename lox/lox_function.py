from lox_callable import LoxCallable
from stmt import Function
from environment import Environment
from exceptions import LoxReturnException


class LoxFunction(LoxCallable):
    def __init__(
        self, declaration: Function, closure: Environment, is_initializer: bool
    ):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def call(self, interpreter: "Interpreter", arguments: list):
        environment: Environment = Environment(self.closure)

        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except LoxReturnException as return_value:
            if self.is_initializer:
                return self.closure.get_at(0, "this")
            return return_value.value

        if self.is_initializer:
            return self.closure.get_at(0, "this")
        return None

    def bind(self, instance: "LoxInstance") -> "LoxFunction":
        environment: Environment = Environment(self.closure)
        environment.define("this", instance)
        return LoxFunction(self.declaration, environment, self.is_initializer)

    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"
