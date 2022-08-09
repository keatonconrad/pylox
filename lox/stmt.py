from expr import Expr
from token import Token

class Stmt:
    def __str__(self) -> str:
        return str(self.expression)

class Expression(Stmt):
    def __init__(self, expr: Expr):
        self.expression = expr

    def accept(self, visitor: "Visitor"):
        return visitor.visit_expression_stmt(self)

class Print(Stmt):
    def __init__(self, expr: Expr):
        self.expression = expr

    def accept(self, visitor: "Visitor"):
        return visitor.visit_print_stmt(self)

class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: "Visitor"):
        return visitor.visit_var_stmt(self)
        