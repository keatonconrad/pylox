from token_type import TokenType

class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: object, line: int):
        self.type: TokenType = type
        self.lexeme: str = lexeme
        self.literal: object = literal
        self.line: int = line

    def __str__(self) -> str:
        return f'{self.type} {self.lexeme} {self.literal}'
    
    def __repr__(self) -> str:
        return f'{self.type} {self.lexeme} {self.literal}'