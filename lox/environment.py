from token import Token
from exceptions import LoxRuntimeError

class Environment:
    def __init__(self):
        self.values: dict = {}

    def define(self, name: str, value: object) -> None:
        self.values[name] = value
    
    def get(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values.get(name.lexeme)
        
        raise LoxRuntimeError(name, f'Undefined variable {name.lexeme}.')

    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        
        raise LoxRuntimeError(name, f'Undefined variable {name.lexeme}.')