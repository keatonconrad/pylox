from token import Token
from expr import Expr, Binary, Unary, Literal, Grouping
from token_type import TokenType
from exceptions import LoxParseError
from typing import Optional

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.current: int = 0
        self.had_error: bool = False

    def parse(self) -> Optional[Expr]:
        try:
            return self.expression()
        except LoxParseError as error:
            error.what()
            return None

    def expression(self) -> Expr:
        return self.equality()
    
    def equality(self) -> Expr:
        expr: Expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator: Token = self.previous()
            right: Expr = self.comparison()
            expr = Binary(expr, operator, right)
        
        return expr

    def comparison(self) -> Expr:
        expr: Expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator: Token = self.previous()
            right: Expr = self.term()
            expr = Binary(expr, operator, right)
        
        return expr

    def term(self) -> Expr:
        expr: Expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator: Token = self.previous()
            right: Expr = self.factor()
            expr = Binary(expr, operator, right)

        return expr
    
    def factor(self) -> Expr:
        expr: Expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator: Token = self.previous()
            right: Expr = self.unary()
            expr = Binary(expr, operator, right)
        
        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator: Token = self.previous()
            right: Expr = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        elif self.match(TokenType.TRUE):
            return Literal(True)
        elif self.match(TokenType.NIL):
            return Literal(None)
        elif self.match(TokenType.NUMBER, TokenType.STRING):
            # We just consumed the number or string in the self.match,
            # so we have to go back and get the previous token's literal
            return Literal(self.previous().literal)
        elif self.match(TokenType.LEFT_PAREN):
            expr: Expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, 'Expect ")" after expression.')
            return Grouping(expr)

        raise self.error(self.peek(), "Expect expression.")

    def match(self, *token_types: TokenType) -> bool:
        # If current token is any of token_types, consume current
        # token and return True
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str) -> LoxParseError:
        self.had_error = True
        parse_error: LoxParseError = LoxParseError(token, message)
        parse_error.what()
        return parse_error

    def synchronize(self) -> None:
        # Discard tokens until it finds a statement boundary

        statement_starts = {
            TokenType.CLASS,                   
            TokenType.FUN,   
            TokenType.VAR,   
            TokenType.FOR,   
            TokenType.IF,    
            TokenType.WHILE, 
            TokenType.PRINT, 
            TokenType.RETURN 
        }

        self.advance()

        while not self.is_at_end:
            if self.previous().type == TokenType.SEMICOLON:
                return
            elif self.peek().type in statement_starts:
                return
            return
    
    def check(self, token_type: TokenType) -> bool:
        # Returns True if current token is of token_type
        if self.is_at_end:
            return False
        return self.peek().type == token_type

    def advance(self) -> Token:
        if not self.is_at_end:
            self.current += 1
        return self.previous()
    
    @property
    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF
    
    def peek(self) -> Token:
        # Returns current token without consuming it
        return self.tokens[self.current]

    def previous(self) -> Token:
        # Returns most recently consumed token
        return self.tokens[self.current - 1]