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
        
class Block(Stmt):
    def __init__(self, statements: list[Stmt]):
        self.statements = statements
    
    def accept(self, visitor: "Visitor"):
        return visitor.visit_block_stmt(self)

class If(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor: "Visitor"):
        return visitor.visit_if_stmt(self)

class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body

    def accept(self, visitor: "Visitor"):
        return visitor.visit_while_stmt(self)