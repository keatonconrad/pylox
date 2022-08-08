from token_type import TokenType
from visitor import Visitor
from expr import Expr, Literal, Grouping, Unary, Binary
from token import Token
from exceptions import LoxRuntimeError

class Interpreter(Visitor):
    def __init__(self):
        self.had_error: bool = False

    def interpret(self, expression: Expr) -> None:
        try:
            value = self.evaluate(expression)
            print(self.stringify(value))
        except LoxRuntimeError:
            return

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_unary_expr(self, expr: Unary):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.BANG:
                return not self.is_truthy(right)
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -float(right)
        
        return None

    def visit_binary_expr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.GREATER:
                self.check_number_operand(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.check_number_operand(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.check_number_operand(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self.check_number_operand(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                elif isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                raise LoxRuntimeError(expr.operator, 'Operands must be two numbers or two strings.')
            case TokenType.SLASH:
                self.check_number_operand(expr.operator, left, right)
                if float(right) == 0:
                    raise LoxRuntimeError(expr.operator, 'Cannot divide by zero.')
                return float(left) / float(right)
            case TokenType.STAR:
                self.check_number_operand(expr.operator, left, right)
                return float(left) * float(right)
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)
        
        return None
    
    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def check_number_operand(self, operator: Token, *operands: object) -> None:
        for operand in operands:
            if not isinstance(operand, float) and not isinstance(operand, int):
                raise LoxRuntimeError(operator, 'Operands must be numbers.')

    def is_truthy(self, obj) -> bool:
        if obj is None:
            return False
        elif isinstance(obj, bool):
            return obj
        return True

    def is_equal(self, left, right) -> bool:
        if left is None and right is None:
            return True
        elif left is None:
            return False
        elif type(left) is not type(right):
            return False
        return left == right
    
    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def stringify(self, obj) -> str:
        if obj is None:
            return 'nil'
        elif obj is False:
            return 'false'
        elif obj is True:
            return 'true'
        elif isinstance(obj, float):
            text: str = str(obj)
            if text.endswith('.0'):
                text = text[:len(text) - 2]
            return text
        return str(obj)
