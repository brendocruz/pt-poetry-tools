from unittest import TestCase
from src.verses.scanner import VerseScanner
from src.verses.tokens import TokenKind
from src.verses.errors import ScanError

class TestScanner(TestCase):

    def test_string(self):
        text    = 'brasil'
        scanner = VerseScanner(text)

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'brasil')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.EOF)




    def test_multiple_string_with_whitespace(self):
        text    = 'minha terra tem palmeiras'
        scanner = VerseScanner(text)

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'minha')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'terra')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'tem')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'palmeiras')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.EOF)




    def test_multiple_whitespace(self):
        text    = 'minha    terra \ntem        \n     palmeiras'
        scanner = VerseScanner(text)

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'minha')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'terra')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'tem')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'palmeiras')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.EOF)




    def test_vowel_operator_tie(self):
        text = 'sa^úde'
        scanner = VerseScanner(text)

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'sa')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.CIRCUMFLEX)
        self.assertEqual(token.value, '^')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'úde')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.EOF)




    def test_vowel_operator_untie(self):
        text = 'sa~udade'
        scanner = VerseScanner(text)

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'sa')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.TILDE)
        self.assertEqual(token.value, '~')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'udade')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.EOF)




    def test_word_operator_tie(self):
        text = 'é_um'
        scanner = VerseScanner(text)

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'é')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.UNDERSCORE)
        self.assertEqual(token.value, '_')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'um')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.EOF)




    def test_word_operator_untie(self):
        text = 'olho*azul'
        scanner = VerseScanner(text)

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'olho')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.ASTERISK)
        self.assertEqual(token.value, '*')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'azul')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.EOF)




    def test_syllable_operator_stress(self):
        text = '>não'
        scanner = VerseScanner(text)

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.GREATER_THAN)
        self.assertEqual(token.value, '>')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'não')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.EOF)




    def test_syllable_operator_unstress(self):
        text = '<não'
        scanner = VerseScanner(text)

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.LESS_THAN)
        self.assertEqual(token.value, '<')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.STRING)
        self.assertEqual(token.value, 'não')

        token = scanner.pop_token()
        self.assertEqual(token.kind, TokenKind.EOF)


    def test_hyphenated_string(self):
        text    = 'água-viva'
        scanner = VerseScanner(text)

        token_A = scanner.pop_token()
        self.assertEqual(token_A.kind, TokenKind.STRING)
        self.assertEqual(token_A.value, 'água')

        token_B = scanner.pop_token()
        self.assertEqual(token_B.kind, TokenKind.STRING)
        self.assertEqual(token_B.value, '-viva')

        token_C = scanner.pop_token()
        self.assertEqual(token_C.kind, TokenKind.EOF)



    def test_double_dash(self):
        text = '--eiro'
        scanner = VerseScanner(text)

        token_A = scanner.pop_token()
        self.assertEqual(token_A.kind, TokenKind.DOUBLE_DASH)
        self.assertEqual(token_A.value, '--')

        token_C = scanner.pop_token()
        self.assertEqual(token_C.kind, TokenKind.STRING)
        self.assertEqual(token_C.value, 'eiro')

        token_D = scanner.pop_token()
        self.assertEqual(token_D.kind, TokenKind.EOF)



    def test_double_dash_and_hyphenated_string(self):
        text = '---eiro'
        scanner = VerseScanner(text)

        token_A = scanner.pop_token()
        self.assertEqual(token_A.kind, TokenKind.DOUBLE_DASH)
        self.assertEqual(token_A.value, '--')

        token_C = scanner.pop_token()
        self.assertEqual(token_C.kind, TokenKind.STRING)
        self.assertEqual(token_C.value, '-eiro')

        token_D = scanner.pop_token()
        self.assertEqual(token_D.kind, TokenKind.EOF)



    def test_scan_dash_error(self):
        text = '-+viva'
        scanner = VerseScanner(text)

        with self.assertRaises(ScanError):
            scanner.pop_token()


    def test_not_supported_character(self):
        text = 'tenho 1 gato, e você?'
        scanner = VerseScanner(text)

        token_A = scanner.pop_token()
        self.assertEqual(token_A.kind, TokenKind.STRING)
        self.assertEqual(token_A.value, 'tenho')

        token_B = scanner.pop_token()
        self.assertEqual(token_B.kind, TokenKind.STRING)
        self.assertEqual(token_B.value, 'gato')

        token_C = scanner.pop_token()
        self.assertEqual(token_C.kind, TokenKind.STRING)
        self.assertEqual(token_C.value, 'e')

        token_D = scanner.pop_token()
        self.assertEqual(token_D.kind, TokenKind.STRING)
        self.assertEqual(token_D.value, 'você')

        token_E = scanner.pop_token()
        self.assertEqual(token_E.kind, TokenKind.EOF)
