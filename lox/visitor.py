from abc import ABC, abstractmethod
from expr import Binary, Grouping, Literal, Unary
from stmt import Expression

class Visitor(ABC):
    @abstractmethod
    def visit_binary_expr(self, expr: Binary):
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr: Grouping):
        pass

    @abstractmethod
    def visit_literal_expr(self, expr: Literal):
        pass
    
    @abstractmethod
    def visit_unary_expr(self, expr: Unary):
        pass

    @abstractmethod
    def visit_expression_stmt(self, stmt: Expression):
        pass