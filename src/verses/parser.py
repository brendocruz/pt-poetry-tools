from typing import Optional
from src.verses.nodes import *
from src.verses.tokens import TokenKind, Token
from src.verses.scanner import VerseScanner
from src.utils.mixins import ReprMixin
from src.verses.errors import ParseError



class VerseParser(ReprMixin):
    scanner: VerseScanner
    lookaheads: tuple[Optional[Token], Optional[Token]]

    def __init__(self, scanner: VerseScanner):
        self.scanner = scanner
        self.lookaheads = (None, None)

    def at_eof(self) -> bool:
        if not self.scanner.at_eof():
            return False
        if not self.lookaheads[0]:
            return True
        if self.lookaheads[0].kind == TokenKind.EOF:
            return True
        return False


    def peek_token(self) -> tuple[Token, Token]:
        lookahead1: Optional[Token] = self.lookaheads[0]
        lookahead2: Optional[Token] = self.lookaheads[1]
        if lookahead1 is None:
            lookahead1 = self.scanner.pop_token()
            lookahead2 = self.scanner.pop_token()
        if lookahead2 is None:
            lookahead2 = self.scanner.pop_token()
        self.lookaheads = (lookahead1, lookahead2)
        return self.lookaheads
        


    def pop_token(self) -> Token:
        tokens = self.peek_token()
        self.lookaheads = (tokens[1], None)
        return tokens[0]


    def pop_or_error(self, target: TokenKind) -> Token:
        result = self.pop_token()
        if result.kind != target:
            index = self.scanner.index
            raise ParseError(index, f'Expected {target}, but got {result.kind}.')
        return result


    def parse_fragment_string(self) -> FragmentString:
        string = self.parse_string()
        fragment = FragmentString(string)
        return fragment


    def parse_fragment_join(self) -> FragmentJoin:
        fragments: list[String] = []
        while True:
            token  = self.pop_or_error(TokenKind.STRING)
            string = String(token.value)
            fragments.append(string)

            lookahead, _ = self.peek_token()
            if lookahead.kind == TokenKind.UNDERSCORE:
                self.pop_token()
                continue
            break
        return FragmentJoin(*fragments)



    def parse_fragment_join_or_fragment_string(self) -> FragmentJoin | FragmentString:
        lookaheads = self.peek_token()
        if lookaheads[1].kind == TokenKind.UNDERSCORE:
            return self.parse_fragment_join()
        return self.parse_fragment_string()



    def parse_fragment_stressed(self) -> FragmentStressed:
        self.pop_or_error(TokenKind.PLUS)
        fragment = self.parse_fragment_join_or_fragment_string()
        stressed = FragmentStressed(fragment)
        return stressed


    def parse_fragment_rest(self) -> FragmentRest:
        self.pop_or_error(TokenKind.DOUBLE_DASH)
        fragment_string = self.parse_string()
        fragment_rest = FragmentRest(fragment_string)
        return fragment_rest




    def parse_fragment(self) -> FragmentString | FragmentJoin | FragmentStressed | FragmentRest:
        lookaheads = self.peek_token()
        if lookaheads[0].kind == TokenKind.PLUS:
            return self.parse_fragment_stressed()
        if lookaheads[0].kind == TokenKind.STRING:
            return self.parse_fragment_join_or_fragment_string()
        if lookaheads[0].kind == TokenKind.DOUBLE_DASH:
            return self.parse_fragment_rest()
        message = 'Could not parse <auto-built-word>'
        raise ParseError(self.scanner.index, message)



    def parse_fragment_word(self) -> Phrase:
        self.pop_or_error(TokenKind.PIPE)
        strings = []
        while True:
            string_token = self.parse_fragment()
            strings.append(string_token)
            self.pop_or_error(TokenKind.PIPE)
            first, second = self.peek_token()
            if first.kind == TokenKind.STRING:
                if second.kind == TokenKind.PIPE:
                    continue
                if second.kind == TokenKind.UNDERSCORE:
                    continue
                break
            if first.kind == TokenKind.PLUS:
                continue
            if first.kind == TokenKind.DOUBLE_DASH:
                continue
            break
        return FragmentWord(*strings)



    def parse_string(self) -> String:
        token  = self.pop_or_error(TokenKind.STRING)
        return String(token.value)



    def parse_auto_word(self) -> Phrase:
        left_token = self.parse_string()
        left_side  = String(left_token.value)
        while True:
            lookahead, _ = self.peek_token()
            if lookahead.kind == TokenKind.CIRCUMFLEX:
                self.pop_token()
                right_token  = self.parse_string()
                right_side = String(right_token.value)
                left_side = PiecesTied(left_side, right_side)
                continue
            if lookahead.kind == TokenKind.TILDE:
                self.pop_token()
                right_token  = self.parse_string()
                right_side = String(right_token.value)
                left_side = PiecesUntied(left_side, right_side)
                continue
            break
        return left_side


    def parse_manual_word(self) -> Phrase:
        self.pop_or_error(TokenKind.OPEN_BRACKET)
        left_token  = self.pop_or_error(TokenKind.STRING)
        left_side = String(left_token.value)
        strings = [left_side]

        while True:
            token = self.pop_token()
            if token.kind == TokenKind.PIPE:
                right_token = self.pop_or_error(TokenKind.STRING)
                right_side  = String(right_token.value)
                strings.append(right_side)
                continue
            if token.kind == TokenKind.CLOSE_BRACKET:
                break
            message = 'Could not parse <auto-built-word>'
            raise ParseError(self.scanner.index, message)
        return ManualWord(*strings)

    

    def parse_stress_word(self) -> Phrase:
        lookahead, _ = self.peek_token()
        if lookahead.kind == TokenKind.GREATER_THAN:
            self.pop_token()
            token = self.pop_or_error(TokenKind.STRING)
            string = String(token.value)
            return StressAll(string)
        if lookahead.kind == TokenKind.LESS_THAN:
            self.pop_token()
            token = self.pop_or_error(TokenKind.STRING)
            string = String(token.value)
            return StressNone(string)
        message = 'Could not parse <stress-altered-word>'
        raise ParseError(self.scanner.index, message)



    def parse_full_word(self):
        lookahead, _ = self.peek_token()
        if lookahead.kind == TokenKind.STRING:
            return self.parse_auto_word()
        if lookahead.kind == TokenKind.PIPE:
            return self.parse_fragment_word()
        if lookahead.kind == TokenKind.OPEN_BRACKET:
            return self.parse_manual_word()
        if lookahead.kind == TokenKind.GREATER_THAN:
            return self.parse_stress_word()
        if lookahead.kind == TokenKind.LESS_THAN:
            return self.parse_stress_word()
        message = 'Could not parse <full-built-word>'
        raise ParseError(self.scanner.index, message)


    def parse_phrase(self) -> Phrase:
        left_phrase = self.parse_full_word()
        while True:
            lookahead, _ = self.peek_token()
            if lookahead.kind == TokenKind.ASTERISK:
                self.pop_token()
                right_phrase = self.parse_full_word()
                left_phrase = WordsTied(left_phrase, right_phrase)
                continue
            if lookahead.kind == TokenKind.SLASH:
                self.pop_token()
                right_phrase = self.parse_full_word()
                left_phrase = WordsUntied(left_phrase, right_phrase)
                continue
            break
        return left_phrase


    def parse_verse(self) -> Verse:
        phrases = []
        while not self.at_eof():
            phrase = self.parse_phrase()
            phrases.append(phrase)
        return Verse(*phrases)


    def parse(self) -> Verse:
        return self.parse_verse()
