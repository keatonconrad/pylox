from token import Token


class Expr:
    pass


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

    def __str__(self) -> str:
        return f"{self.left} {self.operator} {self.right}"


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

    def __str__(self) -> str:
        return f"({self.expression})"


class Literal(Expr):
    def __init__(self, value: object):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)

    def __str__(self) -> str:
        return str(self.value)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)

    def __str__(self) -> str:
        return f"{self.operator} {self.right}"


class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)

    def __str__(self) -> str:
        return str(self.name)


class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign_expr(self)


class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_logical_expr(self)

    def __str__(self) -> str:
        return f"{self.left} {self.operator} {self.right}"


class Call(Expr):
    def __init__(self, callee: Expr, paren: Token, arguments: list[Expr]):
        self.callee = callee
        self.paren = paren  # Used to store this token's location to report function call errors better
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call_expr(self)


class Get(Expr):
    def __init__(self, object: Expr, name: Token):
        self.object = object
        self.name = name

    def accept(self, visitor: "Visitor"):
        return visitor.visit_get_expr(self)


class Set(Expr):
    def __init__(self, object: Expr, name: Token, value: Expr):
        self.object = object
        self.name = name
        self.value = value

    def accept(self, visitor: "Visitor"):
        return visitor.visit_set_expr(self)


class This(Expr):
    def __init__(self, keyword: Token):
        self.keyword = keyword

    def accept(self, visitor: "Visitor"):
        return visitor.visit_this_expr(self)
