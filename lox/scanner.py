from token_type import TokenType
from token import Token
from exceptions import LoxScannerError
import re

class Scanner:

    keywords: dict = {
        'and': TokenType.AND,
        'class': TokenType.CLASS,
        'else': TokenType.ELSE,
        'false': TokenType.FALSE,
        'for': TokenType.FOR,
        'fun': TokenType.FUN,
        'if': TokenType.IF,
        'nil': TokenType.NIL,
        'or': TokenType.OR,
        'return': TokenType.RETURN,
        'super': TokenType.SUPER,
        'this': TokenType.THIS,
        'true': TokenType.TRUE,
        'var': TokenType.VAR,
        'while': TokenType.WHILE,
        'break': TokenType.BREAK,
        'typeof': TokenType.TYPEOF
    }

    def __init__(self, source: str):
        self.had_error: bool = False  # Error state of scanner
        self.source: str = source  # Characters to be tokenized
        self.tokens: list[Token] = []  # Final list of tokens
        self.start: int = 0  # First character in lexeme being scanned
        self.current: int = 0  # Character currently being considered
        self.line: int = 1  # What source line self.current is on

    def scan_tokens(self) -> list[Token]:
        try:
            while not self.is_at_end:
                self.start = self.current
                self.scan_token()
        except LoxScannerError as error:
            self.had_error = True
            error.what()
        else:
            self.tokens.append(Token(TokenType.EOF, '', None, self.line))
            return self.tokens

    def scan_token(self) -> None:
        c: str = self.advance()
        match c:
            case '(': self.add_token(TokenType.LEFT_PAREN)
            case ')': self.add_token(TokenType.RIGHT_PAREN)
            case '{': self.add_token(TokenType.LEFT_BRACE)
            case '}': self.add_token(TokenType.RIGHT_BRACE)
            case ',': self.add_token(TokenType.COMMA)
            case '.': self.add_token(TokenType.DOT)
            case '-': self.add_token(TokenType.MINUS)
            case '+': self.add_token(TokenType.PLUS)
            case ';': self.add_token(TokenType.SEMICOLON)
            case '*': self.add_token(TokenType.STAR)
            case '!': self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            case '=': self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '<': self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>': self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
            case '\n': self.line += 1
            case '"': self.string()
            case ' ' | '\r' | '\t': pass  # Ignore whitespace
            case '/':
                if self.match('/'):
                    # A comment goes until the end of the line
                    while self.peek() != '\n' and not self.is_at_end:
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case _:
                if self.is_digit(c):
                    self.number()
                elif self.is_alpha(c):
                    self.identifier()
                else:
                    raise LoxScannerError(self.line, 'Unexpected character.')

    def identifier(self) -> None:
        while self.is_alphanumeric(self.peek()):
            self.advance()
        
        token_type: TokenType = Scanner.keywords.get(self.current_lexeme)
        if not token_type:
            token_type = TokenType.IDENTIFIER
        self.add_token(token_type)
    
    def number(self) -> None:
        while self.is_digit(self.peek()):
            self.advance()
        
        # Look for a fractional part
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()  # Consume the "."
            while self.is_digit(self.peek()):
                self.advance()
        
            if self.peek() == '.':
                # If lexeme is something like 123.456.78
                raise LoxScannerError(self.line, 'Unexpected character.')
        
        self.add_token(TokenType.NUMBER, float(self.current_lexeme))

    def string(self) -> None:
        while self.peek() != '"' and not self.is_at_end:
            if self.peek() == '\n':
                # Lox allows for multiline strings, so we have to increment
                # the line counter when we hit a new line within the string
                self.line += 1
            self.advance()
        
        if self.is_at_end:
            raise LoxScannerError(self.line, "Unterminated string.")

        self.advance()  # The closing "

        # Trim the surrounding quotes
        value: str = self.source[self.start + 1: self.current - 1]
        self.add_token(TokenType.STRING, value)

    def match(self, expected: str) -> bool:
        if self.is_at_end:
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end:
            return '\0'
        return self.source[self.current]
    
    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def is_alpha(self, c: str) -> bool:
        return re.match(r'[A-Za-z0-9_]+$', c)
    
    def is_alphanumeric(self, c: str) -> bool:
        return self.is_alpha(c) or self.is_digit(c)

    def is_digit(self, c: str) -> bool:
        return re.match(r'[0-9]+$', c)

    @property
    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    @property
    def current_lexeme(self) -> str:
        return self.source[self.start:self.current]

    def advance(self) -> str:
        # Consumes a character and returns the consumed character
        if self.is_at_end:
            return ''
        
        self.current += 1
        return self.source[self.current - 1]
    
    def add_token(self, type: TokenType, literal: object = None) -> None:
        self.tokens.append(Token(type, self.current_lexeme, literal, self.line))