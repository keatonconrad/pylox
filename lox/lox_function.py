from lox_callable import LoxCallable
from stmt import Function
from environment import Environment

class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function):
        self.declaration = declaration

    def call(self, interpreter: "Interpreter", arguments: list):
        environment: Environment = Environment(interpreter.globals)

        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        
        interpreter.execute_block(self.declaration.body, environment)
        return None
    
    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self) -> str:
        return f'<fn {self.declaration.name.lexeme}>'