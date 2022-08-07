import sys
import typing
from scanner import Scanner
from token import Token

class Lox:
    had_error: bool = False

    @classmethod
    def run_file(cls, path: str) -> None:
        file: typing.TextIO = open(path, 'rt')
        cls.run(file.read())
        file.close()
        if cls.had_error:
            sys.exit(65)
    
    @classmethod
    def run_prompt(cls) -> None:
        while True:
            line: str = input('Lox > ')
            if not line:
                break
            cls.run(line)
            cls.had_error = False

    @classmethod
    def run(cls, source: str) -> None:
        scanner: Scanner = Scanner(source)
        tokens: list[Token] = scanner.scan_tokens()

        if scanner.had_error:
            cls.had_error = True
            return

        for token in tokens:
            print(token)

if __name__ == '__main__':
    if len(sys.argv) > 2:
        print('Usage: pylox [script]')
        sys.exit(64)
    elif len(sys.argv) == 2:
        Lox.run_file(sys.argv[1])
    else:
        Lox.run_prompt()