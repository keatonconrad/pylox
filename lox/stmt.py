from expr import Expr, Variable
from token import Token


class Stmt:
    pass


class Expression(Stmt):
    def __init__(self, expr: Expr):
        self.expression = expr

    def accept(self, visitor: "Visitor"):
        return visitor.visit_expression_stmt(self)


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


class Break(Stmt):
    def __init__(self):
        pass

    def accept(self, visitor: "Visitor"):
        return visitor.visit_break_stmt(self)


class Function(Stmt):
    def __init__(self, name: Token, params: list[Token], body: list[Stmt]):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor: "Visitor"):
        return visitor.visit_function_stmt(self)


class Return(Stmt):
    def __init__(self, keyword: Token, value: Expr):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor: "Visitor"):
        return visitor.visit_return_stmt(self)


class Class(Stmt):
    def __init__(self, name: Token, superclass: Variable, methods: list[Function]):
        self.name = name
        self.methods = methods
        self.superclass = superclass

    def accept(self, visitor: "Visitor"):
        return visitor.visit_class_stmt(self)
