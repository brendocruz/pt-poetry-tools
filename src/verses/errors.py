class ScanError(Exception):
    def __init__(self, index: int, message: str):
        super().__init__(f'{message} [at {index}]')
        self.index = index


class ParseError(Exception):
    def __init__(self, index: int, message: str):
        super().__init__(f'{message} [at {index}]')
        self.index = index
