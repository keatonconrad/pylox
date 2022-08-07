from abc import ABC, abstractmethod
from expr import Expr, Binary, Grouping, Literal, Unary

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