class LoxException(Exception):
    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print(f'[line {line}] Error{where}: {message}')

    def what(self):
        pass

class LoxScannerError(LoxException):
    def __init__(self, line: int, message: str):
        self.line = line
        self.message = message
    
    def what(self):
        return self.report(self.line, '', self.message)