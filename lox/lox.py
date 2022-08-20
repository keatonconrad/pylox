import sys
import typing
from interpreter import Interpreter
from stmt import Stmt
from scanner import Scanner
from token import Token
from parser import Parser
from resolver import Resolver


class Lox:
    had_error: bool = False
    had_runtime_error: bool = False

    interpreter: Interpreter = Interpreter()

    @classmethod
    def run_file(cls, path: str) -> None:
        file: typing.TextIO = open(path, "rt")
        cls.run(file.read())
        file.close()
        if cls.had_error:
            sys.exit(65)
        if cls.had_runtime_error:
            sys.exit(70)

    @classmethod
    def run_prompt(cls) -> None:
        while True:
            line: str = input("Lox > ")
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

        parser: Parser = Parser(tokens)
        statements: list[Stmt] = parser.parse()

        if parser.had_error:
            cls.had_error = True
            return

        resolver: Resolver = Resolver(cls.interpreter)
        resolver.resolve(statements)

        if resolver.had_error:
            cls.had_error = True
            return

        # print(tokens)
        # AstPrinter().print(expression)
        cls.interpreter.interpret(statements)

        if cls.interpreter.had_error:
            cls.had_runtime_error = True
            return


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: pylox [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        Lox.run_file(sys.argv[1])
    else:
        Lox.run_prompt()
