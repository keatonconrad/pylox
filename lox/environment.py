from token import Token
from exceptions import LoxRuntimeError


class Environment:
    def __init__(self, enclosing: "Environment" = None):
        self.values: dict = {}
        self.enclosing: Environment = enclosing

    def define(self, name: str, value: object) -> None:
        self.values[name] = value

    def get_at(self, distance: int, name: str) -> object:
        # Returns the value of the variable in the corrent environment's dict
        return self.ancestor(distance).values.get(name)

    def ancestor(self, distance: int) -> "Environment":
        # Returns the environment at distance away from this environment
        environment: Environment = self
        for i in range(distance):
            environment = environment.enclosing
        return environment

    def get(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values.get(name.lexeme)

        if self.enclosing:
            return self.enclosing.get(name)

        raise LoxRuntimeError(name, f"Undefined variable {name.lexeme}.")

    def assign_at(self, distance: int, name: Token, value: object) -> None:
        self.ancestor(distance).values[name.lexeme] = value

    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing:
            self.enclosing.assign(name, value)
            return

        raise LoxRuntimeError(name, f"Undefined variable {name.lexeme}.")
