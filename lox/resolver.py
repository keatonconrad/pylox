from typing import Union
from expr import Expr, Variable, Assign, Binary, Call, Grouping, Literal, Logical, Unary
from visitor import Visitor
from stmt import Stmt, Block, Var, Function, Expression, If, Return, While
from token import Token
from exceptions import LoxStaticError
from enum import Enum


class FunctionType(Enum):
    NONE = 0
    FUNCTION = 1


class Resolver(Visitor):
    def __init__(self, interpreter: "Interpreter"):
        self.interpreter = interpreter
        self.scopes: list[dict[str, bool]] = []
        self.current_function = FunctionType.NONE
        self.had_error: bool = False

    def visit_block_stmt(self, stmt: Block) -> None:
        self.begin_scope()
        self.resolve_list(stmt.statements)
        self.end_scope()

    def visit_var_stmt(self, stmt: Var) -> None:
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)
        self.define(stmt.name)

    def visit_function_stmt(self, stmt: Function) -> None:
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)

    def visit_if_stmt(self, stmt: If) -> None:
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve(stmt.else_branch)

    def visit_while_Stmt(self, stmt: While) -> None:
        self.resolve(stmt.condition)
        self.resolve(stmt.body)

    def visit_return_stmt(self, stmt: Return) -> None:
        if self.current_function == FunctionType.NONE:
            LoxStaticError(stmt.keyword, "Can't return from top-level code.").what()
            self.had_error = True
        if stmt.value is not None:
            self.resolve(stmt.value)

    def visit_expression_stmt(self, stmt: Expression) -> None:
        self.resolve(stmt.expression)

    def visit_variable_expr(self, expr: Variable) -> None:
        if len(self.scopes) > 0 and self.scopes[-1].get(expr.name.lexeme) is False:
            LoxStaticError(
                expr.name, "Can't read local variable in its own initializer."
            ).what()
            self.had_error = True

    def visit_assign_expr(self, expr: Assign) -> None:
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)

    def visit_binary_expr(self, expr: Binary) -> None:
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_call_expr(self, expr: Call) -> None:
        self.resolve(expr.callee)
        for argument in expr.arguments:
            self.resolve(argument)

    def visit_grouping_expr(self, expr: Grouping) -> None:
        self.resolve(expr.expression)

    def visit_logical_expr(self, expr: Logical) -> None:
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_unary_expr(self, expr: Unary) -> None:
        self.resolve(expr.right)

    def visit_literal_expr(self, expr: Literal) -> None:
        return None

    def resolve_list(self, statements: list[Stmt]) -> None:
        for stmt in statements:
            self.resolve(stmt)

    def resolve(self, obj: Union[Stmt, Expr]) -> None:
        obj.accept(self)

    def resolve_function(self, function: Function, function_type: FunctionType) -> None:
        enclosing_function: FunctionType = self.current_function
        self.current_function = function_type
        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.end_scope()
        # When we're done resolving the function body, restore the current function
        # to the enclosing function
        self.current_function = enclosing_function

    def resolve_local(self, expr: Expr, name: Token) -> None:
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return

    def begin_scope(self) -> None:
        self.scopes.append({})

    def end_scope(self) -> None:
        self.scopes.pop()

    def declare(self, name: Token) -> None:
        if len(self.scopes) == 0:
            return

        if name.lexeme in self.scopes[-1]:
            LoxStaticError(
                name, "Already a variable with this name in this scope."
            ).what()
            self.had_error = True
        else:
            # False meaning we have not finished resolving the variable's initializer
            self.scopes[-1][name.lexeme] = False

    def define(self, name: Token) -> None:
        if len(self.scopes) == 0:
            return

        self.scopes[-1][name.lexeme] = True