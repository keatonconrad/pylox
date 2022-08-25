from environment import Environment
from lox_callable import LoxCallable
from stmt import Expression, Stmt, Var, Block, If, While, Break, Function, Return, Class
from token_type import TokenType
from visitor import Visitor
from expr import (
    Expr,
    Literal,
    Grouping,
    Unary,
    Binary,
    Variable,
    Assign,
    Logical,
    Call,
    Get,
    Set,
    This,
)
from token import Token
from exceptions import LoxRuntimeError, LoxBreakException, LoxReturnException
import time
from lox_function import LoxFunction
from lox_class import LoxClass
from lox_instance import LoxInstance


class Interpreter(Visitor):
    def __init__(self):
        self.had_error: bool = False
        self.globals: Environment = Environment()  # Global scope
        # Current scope starts as global scope
        self.environment: Environment = self.globals
        self.locals: dict = {}

        class Clock(LoxCallable):
            def arity(self):
                return 0

            def call(self, interpreter: Interpreter, arguments: list = []):
                return time.process_time()

            def __str__(self):
                return '<native function "clock">'

        class Print(LoxCallable):
            def arity(self):
                return 1

            def call(self, interpreter: Interpreter, arguments: list = []):
                message = interpreter.stringify(arguments[0])
                print(message)

            def __str__(self):
                return '<native function "print">'

        self.globals.define("clock", Clock())
        self.globals.define("print", Print())

    def interpret(self, statements: list[Stmt]) -> None:
        try:
            for statement in statements:
                self.execute(statement)
        except LoxRuntimeError as error:
            error.what()
            return

    def visit_call_expr(self, expr: Call):
        callee = self.evaluate(expr.callee)

        arguments: list = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        if not isinstance(callee, LoxCallable):
            raise LoxRuntimeError(expr.paren, "Can only call functions and classes.")

        if len(arguments) != callee.arity():
            raise LoxRuntimeError(
                expr.paren,
                f"Expected {callee.arity()} arguments but got {len(arguments)}.",
            )

        return callee.call(self, arguments)

    def visit_get_expr(self, expr: Get):
        object_ = self.evaluate(expr.object)
        if isinstance(object_, LoxInstance):
            return object_.get(expr.name)

        raise LoxRuntimeError(expr.name, "Only instances have properties.")

    def visit_set_expr(self, expr: Set):
        object_ = self.evaluate(expr.object)

        if not isinstance(object_, LoxInstance):
            raise LoxRuntimeError(expr.name, "Only instances have fields.")

        value = self.evaluate(expr.value)
        object_.set(expr.name, value)
        return value

    def visit_this_expr(self, expr: This):
        return self.look_up_variable(expr.keyword, expr)

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
                raise LoxRuntimeError(
                    expr.operator, "Operands must be two numbers or two strings."
                )
            case TokenType.SLASH:
                self.check_number_operand(expr.operator, left, right)
                if float(right) == 0:
                    raise LoxRuntimeError(expr.operator, "Cannot divide by zero.")
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

    def visit_variable_expr(self, expr: Variable) -> Expr:
        return self.look_up_variable(expr.name, expr)

    def visit_assign_expr(self, expr: Assign) -> Expr:
        value = self.evaluate(expr.value)

        distance: int = self.locals.get(expr)
        if distance is not None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)

        return value

    def visit_logical_expr(self, expr: Logical):
        left = self.evaluate(expr.left)

        if expr.operator.type == TokenType.OR:
            # If or statement
            if self.is_truthy(left):
                return left
        else:
            # If and statement
            if not self.is_truthy(left):
                return left

        return self.evaluate(expr.right)

    def visit_expression_stmt(self, stmt: Expression) -> None:
        self.evaluate(stmt.expression)

    def visit_function_stmt(self, stmt: Function) -> None:
        function: LoxFunction = LoxFunction(stmt, self.environment, False)
        self.environment.define(stmt.name.lexeme, function)

    def visit_return_stmt(self, stmt: Return) -> None:
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise LoxReturnException(value)

    def visit_while_stmt(self, stmt: While) -> None:
        try:
            while self.is_truthy(self.evaluate(stmt.condition)):
                self.execute(stmt.body)
        except LoxBreakException:
            pass

    def visit_break_stmt(self, stmt: Break) -> None:
        raise LoxBreakException()

    def visit_block_stmt(self, stmt: Block) -> None:
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_var_stmt(self, stmt: Var) -> None:
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)

    def visit_if_stmt(self, stmt: If) -> None:
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_class_stmt(self, stmt: Class) -> None:
        self.environment.define(stmt.name.lexeme, None)
        methods: dict[str, LoxFunction] = {}
        for method in stmt.methods:
            methods[method.name.lexeme] = LoxFunction(
                method, self.environment, method.name.lexeme == "init"
            )
        klass: LoxClass = LoxClass(stmt.name.lexeme, methods)
        self.environment.assign(stmt.name, klass)

    def look_up_variable(self, name: Token, expr: Expr) -> None:
        distance: int = self.locals.get(expr)
        if distance is not None:
            return self.environment.get_at(distance, name.lexeme)
        else:
            return self.globals.get(name)

    def check_number_operand(self, operator: Token, *operands: object) -> None:
        for operand in operands:
            if not isinstance(operand, float) and not isinstance(operand, int):
                raise LoxRuntimeError(operator, "Operands must be numbers.")

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

    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def execute_block(self, statements: list[Stmt], environment: Environment) -> None:
        previous: Environment = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def resolve(self, expr: Expr, depth: int) -> None:
        self.locals[expr] = depth

    def stringify(self, obj) -> str:
        if obj is None:
            return "nil"
        elif obj is False:
            return "false"
        elif obj is True:
            return "true"
        elif isinstance(obj, float):
            text: str = str(obj)
            if text.endswith(".0"):
                text = text[: len(text) - 2]
            return text
        return str(obj)
