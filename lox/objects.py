from lox_class import LoxClass
from stmt import Function, Return
from expr import Literal
from lox_function import LoxFunction
from token import Token
from token_type import TokenType
from environment import Environment

global_environment = Environment()

base_object = LoxClass(
    name="object",
    superclass=None,
    methods={
        "test": LoxFunction(
            declaration=Function(
                Token(TokenType.IDENTIFIER, "test", None, 1),
                [],
                [Return(Token(TokenType.RETURN, "return", None, 1), Literal(3))],
            ),
            closure=global_environment,
            is_initializer=False,
        ),
    },
)

number_object = LoxClass(
    name="number",
    superclass=base_object,
    methods={},
)
