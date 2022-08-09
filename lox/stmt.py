from expr import Expr

class Stmt:
    pass

class Expression(Stmt):
    def __init__(self, expr: Expr):
        self.expression = expr

    def accept(self, visitor: "Visitor"):
        return visitor.visit_expression_stmt(self)
    
    def __str__(self) -> str:
        return str(self.expression)

class Print(Stmt):
    def __init__(self, expr: Expr):
        self.expression = expr

    def accept(self, visitor: "Visitor"):
        return visitor.visit_print_stmt(self)
    
    def __str__(self) -> str:
        return str(self.expression)