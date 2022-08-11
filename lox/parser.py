from token import Token
from expr import Expr, Binary, Unary, Literal, Grouping, Variable, Assign, Logical
from stmt import Stmt, Print, Expression, Var, Block, If, While
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
            statements: list[Stmt] = []
            while not self.is_at_end:
                statements.append(self.declaration())
            return statements
        except LoxParseError as error:
            error.what()
            return None

    def declaration(self) -> Optional[Stmt]:
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except LoxParseError:
            self.synchronize()

    def var_declaration(self) -> Stmt:
        name: Token = self.consume(TokenType.IDENTIFIER, 'Expect variable name.')

        # Sets up optional initialized value
        initializer: Expr = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        
        self.consume(TokenType.SEMICOLON, 'Expect ";" after variable declaration.')
        return Var(name, initializer)

    def statement(self) -> Stmt:
        if self.match(TokenType.PRINT):
            return self.print_statement()
        elif self.match(TokenType.WHILE):
            return self.while_statement()
        elif self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        elif self.match(TokenType.IF):
            return self.if_statement()
        return self.expression_statement()

    def while_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, 'Expect "(" after "while".')
        condition: Expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, 'Expect ")" after condition.')
        body: Stmt = self.statement()
        
        return While(condition, body)

    def if_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, 'Expect "(" after "if".')
        condition: Expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, 'Expect ")" after if condition.')

        then_branch: Stmt = self.statement()
        else_branch: Stmt = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()
        
        return If(condition, then_branch, else_branch)

    def print_statement(self) -> Stmt:
        value: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, 'Expect ";" after value.')
        return Print(value)

    def expression_statement(self) -> Stmt:
        expr: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, 'Expect ";" after expression.')
        return Expression(expr)

    def block(self) -> list[Stmt]:
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end:
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, 'Expect "}" after block.')
        return statements

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr: Expr = self.or_expr()

        if self.match(TokenType.EQUAL):
            equals: Token = self.previous()
            value: Expr = self.assignment()

            if isinstance(expr, Variable):
                return Assign(expr.name, value)
            
            LoxParseError(equals, 'Invalid assignment target.').what()
        
        return expr

    def or_expr(self) -> Expr:
        expr: Expr = self.and_expr()

        while self.match(TokenType.OR):
            operator: Token = self.previous()
            right: Expr = self.and_expr()
            expr = Logical(expr, operator, right)

        return expr

    def or_expr(self) -> Expr:
        expr: Expr = self.equality()

        while self.match(TokenType.AND):
            operator: Token = self.previous()
            right: Expr = self.equality()
            expr = Logical(expr, operator, right)

        return expr
    
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
        elif self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
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