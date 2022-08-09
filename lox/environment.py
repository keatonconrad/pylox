from token import Token
from exceptions import LoxRuntimeError

class Environment:
    def __init__(self, enclosing: "Environment" = None):
        self.values: dict = {}
        self.enclosing: Environment = enclosing

    def define(self, name: str, value: object) -> None:
        self.values[name] = value
    
    def get(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values.get(name.lexeme)

        if self.enclosing:
            return self.enclosing.get(name)
        
        raise LoxRuntimeError(name, f'Undefined variable {name.lexeme}.')

    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        
        raise LoxRuntimeError(name, f'Undefined variable {name.lexeme}.')