from visitor import Visitor
from expr import Expr, Binary, Grouping, Literal, Unary
from token_type import TokenType
from token import Token


class AstPrinter(Visitor):
    def __init__(self):
        pass

    def print(self, expr: Expr) -> str:
        return print(expr.accept(self))

    def visit_binary_expr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        builder: str = f"({name}"
        for expr in exprs:
            builder += f" {expr.accept(self)}"
        builder += ")"
        return builder


if __name__ == "__main__":
    printer = AstPrinter()
    expression: Expr = Binary(
        Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67)),
    )

    printer.print(expression)
