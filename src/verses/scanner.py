from src.verses.tokens import Token, TokenKind, LETTER_CHARACTERS
from src.utils.mixins import ReprMixin
from src.verses.errors import ScanError

WHITESPACE_CHARACTERES = frozenset([' ', '\t', '\n', '\r'])

class VerseScanner(ReprMixin):

    def __init__(self, verse: str):
        self.verse = verse
        self.length = len(verse)
        self.index = 0


    def at_eof(self):
        return self.index >= self.length


    def pop_char(self):
        char = self.verse[self.index]
        self.index += 1
        return char


    def peek_char(self):
        char = self.verse[self.index]
        return char


    def is_letter(self, char: str):
        return char in LETTER_CHARACTERS

    def is_whitespace(self, char: str):
        return char in WHITESPACE_CHARACTERES

    def scan_whitespace(self) -> None:
        while not self.at_eof():
            char = self.peek_char()
            if self.is_whitespace(char):
                self.pop_char()
                continue
            break

    def scan_dash(self, start_char) -> Token:
        if self.peek_char() == '-':
            char  = self.pop_char()
            chars = [start_char]
            chars.append(char)
            string = ''.join(chars)
            return Token(TokenKind.DOUBLE_DASH, string)
        if self.is_letter(self.peek_char()):
            return self.scan_string(start_char)
        message = f'Unexpected `{self.peek_char()}` after `{start_char}`'
        raise ScanError(self.index, message)


    def scan_string(self, start_char) -> Token:
        chars = [start_char]
        while not self.at_eof():
            char = self.peek_char()
            if self.is_letter(char):
                self.pop_char()
                chars.append(char)
                continue
            break
        string = ''.join(chars)
        return Token(TokenKind.STRING, string)


    def pop_token(self) -> Token:
        if self.at_eof():
            return Token(TokenKind.EOF, '')

        char = self.pop_char()
        if char == '^':
            return Token(TokenKind.CIRCUMFLEX, char)
        if char == '~':
            return Token(TokenKind.TILDE, char)
        if char == '/':
            return Token(TokenKind.SLASH, char)
        if char == '*':
            return Token(TokenKind.ASTERISK, char)
        if char == '_':
            return Token(TokenKind.UNDERSCORE, char)
        if char == '<':
            return Token(TokenKind.LESS_THAN, char)
        if char == '>':
            return Token(TokenKind.GREATER_THAN, char)
        if char == '+':
            return Token(TokenKind.PLUS, char)
        if char == '[':
            return Token(TokenKind.OPEN_BRACKET, char)
        if char == ']':
            return Token(TokenKind.CLOSE_BRACKET, char)
        if char == '|':
            return Token(TokenKind.PIPE, char)
        if char == '-':
            return self.scan_dash(char)
        if self.is_letter(char):
            return self.scan_string(char)
        if self.is_whitespace(char):
            self.scan_whitespace()
            return self.pop_token()
        return self.pop_token()
