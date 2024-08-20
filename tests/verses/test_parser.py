from unittest import TestCase
from src.verses.scanner import VerseScanner
from src.verses.parser import ParseError, VerseParser
from src.verses.nodes import *


class TestParser(TestCase):

    def test_empty(self):
        input   = ''
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse = parser.parse()
        self.assertEqual(len(verse.children), 0)



    def test_string_single(self):
        input   = 'vermelho'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse = parser.parse()
        self.assertEqual(len(verse.children), 1)

        string = verse.children[0]
        self.assertIsInstance(string, String)



    def test_string_multiple(self):
        input   = 'vermelho verde azul'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse = parser.parse()
        self.assertEqual(len(verse.children), 3)

        string_1 = verse.children[0]
        self.assertEqual(string_1, String('vermelho'))
        string_2 = verse.children[1]
        self.assertEqual(string_2, String('verde'))
        string_3 = verse.children[2]
        self.assertEqual(string_3, String('azul'))



    def test_string_hyphenated(self):
        input   = 'água-viva'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse = parser.parse()

        self.assertEqual(len(verse.children), 2)
        self.assertEqual(verse.children[0], String('água'))
        self.assertEqual(verse.children[1], String('-viva'))



    def test_stress_all(self):
        input   = '> amarelo'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse = parser.parse()


        all_stress = verse.children[0]
        self.assertIsInstance(all_stress, StressAll)
        string = all_stress.children[0]
        self.assertEqual(string, String('amarelo'))



    def test_stress_none(self):
        input   = '< verde'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse = parser.parse()

        all_unstress = verse.children[0]
        self.assertIsInstance(all_unstress, StressNone)
        string = all_unstress.children[0]
        self.assertEqual(string, String('verde'))



    def test_vowels_tied(self):
        input   = 'sa ^ udade'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse = parser.parse()

        auto_word = verse.children[0]
        self.assertIsInstance(auto_word, PiecesTied)
        self.assertEqual(len(auto_word.children), 2)

        string_1 = auto_word.children[0]
        self.assertEqual(string_1, String('sa'))
        string_2 = auto_word.children[1]
        self.assertEqual(string_2, String('udade'))



    def test_vowels_untied(self):
        input   = 'sa ~ úde'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse = parser.parse()

        auto_word = verse.children[0]
        self.assertIsInstance(auto_word, PiecesUntied)
        self.assertEqual(len(auto_word.children), 2)

        string_1 = auto_word.children[0]
        self.assertEqual(string_1, String('sa'))
        string_2 = auto_word.children[1]
        self.assertEqual(string_2, String('úde'))



    def test_vowels_tied_and_untied(self):
        input   = 'sa ^ uda ~ de'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse = parser.parse()

        child_A = verse.children[0]
        self.assertIsInstance(child_A, PiecesUntied)
        self.assertEqual(len(child_A.children), 2)

        child_A_1 = child_A.children[0]
        self.assertIsInstance(child_A_1, PiecesTied)
        self.assertEqual(len(child_A_1.children), 2)
        self.assertEqual(child_A_1.children[0], String('sa'))
        self.assertEqual(child_A_1.children[1], String('uda'))

        child_A_2 = child_A.children[1]
        self.assertEqual(child_A_2, String('de'))



    def test_fragment_word(self):
        input   = '| a | ma | re | lo |'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse   = parser.parse()

        child_A = verse.children[0]
        self.assertIsInstance(child_A, FragmentWord)
        self.assertEqual(len(child_A.children), 4)

        child_A_1 = child_A.children[0]
        self.assertIsInstance(child_A_1, FragmentString)
        self.assertEqual(len(child_A_1.children), 1)
        self.assertEqual(child_A_1.children[0], String('a'))

        child_A_2 = child_A.children[1]
        self.assertIsInstance(child_A_2, FragmentString)
        self.assertEqual(len(child_A_2.children), 1)
        self.assertEqual(child_A_2.children[0], String('ma'))

        child_A_3 = child_A.children[2]
        self.assertIsInstance(child_A_3, FragmentString)
        self.assertEqual(len(child_A_3.children), 1)
        self.assertEqual(child_A_3.children[0], String('re'))

        child_A_4 = child_A.children[3]
        self.assertIsInstance(child_A_4, FragmentString)
        self.assertEqual(len(child_A_4.children), 1)
        self.assertEqual(child_A_4.children[0], String('lo'))



    def test_fragment_stressed_string(self):
        input   = '| a | ma | +re | lo_e | +a | zul |'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse   = parser.parse()

        self.assertEqual(len(verse.children), 1)

        child_A = verse.children[0]
        self.assertIsInstance(child_A, FragmentWord)
        self.assertEqual(len(child_A.children), 6)

        child_A_1 = child_A.children[0]
        self.assertIsInstance(child_A_1, FragmentString)
        self.assertEqual(len(child_A_1.children), 1)
        self.assertEqual(child_A_1.children[0], String('a'))

        child_A_2 = child_A.children[1]
        self.assertIsInstance(child_A_2, FragmentString)
        self.assertEqual(len(child_A_2.children), 1)
        self.assertEqual(child_A_2.children[0], String('ma'))

        child_A_3 = child_A.children[2]
        self.assertIsInstance(child_A_3, FragmentStressed)
        self.assertEqual(len(child_A_3.children), 1)
        child_A_3_1 = child_A_3.children[0]
        self.assertIsInstance(child_A_3_1, FragmentString)
        self.assertEqual(len(child_A_3_1.children), 1)
        self.assertEqual(child_A_3_1.children[0], String('re'))

        child_A_4 = child_A.children[3]
        self.assertIsInstance(child_A_4, FragmentJoin)
        self.assertEqual(len(child_A_4.children), 2)
        self.assertEqual(child_A_4.children[0], String('lo'))
        self.assertEqual(child_A_4.children[1], String('e'))

        child_A_5 = child_A.children[4]
        self.assertIsInstance(child_A_5, FragmentStressed)
        self.assertEqual(len(child_A_5.children), 1)
        child_A_5_1 = child_A_5.children[0]
        self.assertIsInstance(child_A_5_1, FragmentString)
        self.assertEqual(len(child_A_5_1.children), 1)
        self.assertEqual(child_A_5_1.children[0], String('a'))

        child_A_6 = child_A.children[5]
        self.assertIsInstance(child_A_6, FragmentString)
        self.assertEqual(len(child_A_6.children), 1)
        self.assertEqual(child_A_6.children[0], String('zul'))



    def test_fragment_join(self):
        input   = '| ca | sa_a_a | zul|'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse   = parser.parse()

        self.assertEqual(len(verse.children), 1)

        child_A = verse.children[0]
        self.assertIsInstance(child_A, FragmentWord)
        self.assertEqual(len(child_A.children), 3)

        child_A_1 = child_A.children[0]
        self.assertIsInstance(child_A_1, FragmentString)
        self.assertEqual(len(child_A_1.children), 1)
        self.assertEqual(child_A_1.children[0], String('ca'))

        child_A_2 = child_A.children[1]
        self.assertIsInstance(child_A_2, FragmentJoin)
        self.assertEqual(len(child_A_2.children), 3)
        self.assertEqual(child_A_2.children[0], String('sa'))
        self.assertEqual(child_A_2.children[1], String('a'))
        self.assertEqual(child_A_2.children[2], String('a'))

        child_A_3 = child_A.children[2]
        self.assertIsInstance(child_A_3, FragmentString)
        self.assertEqual(len(child_A_3.children), 1)
        self.assertEqual(child_A_3.children[0], String('zul'))



    def test_fragment_stressed_join(self):
        input   = '|pa|le|+tó_a|+zul|'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse   = parser.parse()

        self.assertEqual(len(verse.children), 1)

        child_A = verse.children[0]
        self.assertIsInstance(child_A, FragmentWord)
        self.assertEqual(len(child_A.children), 4)

        child_A_1 = child_A.children[0]
        self.assertIsInstance(child_A_1, FragmentString)
        self.assertEqual(len(child_A_1.children), 1)
        self.assertEqual(child_A_1.children[0], String('pa'))

        child_A_2 = child_A.children[1]
        self.assertIsInstance(child_A_2, FragmentString)
        self.assertEqual(len(child_A_2.children), 1)
        self.assertEqual(child_A_2.children[0], String('le'))

        child_A_3 = child_A.children[2]
        self.assertIsInstance(child_A_3, FragmentStressed)
        self.assertEqual(len(child_A_3.children), 1)

        child_A_3_1 = child_A_3.children[0]
        self.assertIsInstance(child_A_3_1, FragmentJoin)
        self.assertEqual(len(child_A_3_1.children), 2)
        self.assertEqual(child_A_3_1.children[0], String('tó'))
        self.assertEqual(child_A_3_1.children[1], String('a'))

        child_A_4 = child_A.children[3]
        self.assertIsInstance(child_A_4, FragmentStressed)
        self.assertEqual(len(child_A_4.children), 1)

        child_A_4_1 = child_A_4.children[0]
        self.assertIsInstance(child_A_4_1, FragmentString)
        self.assertEqual(child_A_4_1.children[0], String('zul'))



    def test_fragment_hyphenated_string(self):
        text   = '|trem|-ba|la|'
        scanner = VerseScanner(text)
        parser  = VerseParser(scanner)
        verse = parser.parse()

        self.assertEqual(len(verse.children), 1)



    def test_fragment_word_with_rest(self):
        input   = '|ma|te|má|--tica|'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse   = parser.parse()

        child_A = verse.children[0]
        self.assertIsInstance(child_A, FragmentWord)
        self.assertEqual(len(child_A.children), 4)

        child_A_1 = child_A.children[0]
        self.assertIsInstance(child_A_1, FragmentString)
        self.assertEqual(len(child_A_1.children), 1)
        self.assertEqual(child_A_1.children[0], String('ma'))

        child_A_2 = child_A.children[1]
        self.assertIsInstance(child_A_2, FragmentString)
        self.assertEqual(len(child_A_2.children), 1)
        self.assertEqual(child_A_2.children[0], String('te'))

        child_A_3 = child_A.children[2]
        self.assertIsInstance(child_A_3, FragmentString)
        self.assertEqual(len(child_A_3.children), 1)
        self.assertEqual(child_A_3.children[0], String('má'))

        child_A_4 = child_A.children[3]
        self.assertIsInstance(child_A_4, FragmentRest)
        self.assertEqual(len(child_A_4.children), 1)
        self.assertEqual(child_A_4.children[0], String('tica'))




    def test_words_tied(self):
        input   = 'amarelo * azul'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse = parser.parse()

        fragment_word = verse.children[0]
        self.assertIsInstance(fragment_word, WordsTied)
        self.assertEqual(len(fragment_word.children), 2)

        string_1 = fragment_word.children[0]
        self.assertEqual(string_1, String('amarelo'))
        string_2 = fragment_word.children[1]
        self.assertEqual(string_2, String('azul'))



    def test_words_untied(self):
        input   = 'amarelo / azul'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse = parser.parse()

        fragment_word = verse.children[0]
        self.assertIsInstance(fragment_word, WordsUntied)
        self.assertEqual(len(fragment_word.children), 2)

        string_1 = fragment_word.children[0]
        self.assertEqual(string_1, String('amarelo'))
        string_2 = fragment_word.children[1]
        self.assertEqual(string_2, String('azul'))



    def test_manual_word(self):
        input   = '[ ver | me | lho ]'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse = parser.parse()

        manual_word = verse.children[0]
        self.assertIsInstance(manual_word, ManualWord)
        self.assertEqual(len(manual_word.children), 3)

        string_1 = manual_word.children[0]
        self.assertEqual(string_1, String('ver'))
        string_2 = manual_word.children[1]
        self.assertEqual(string_2, String('me'))
        string_3 = manual_word.children[2]
        self.assertEqual(string_3, String('lho'))



    def test_manual_word_malformed_1(self):
        input   = '[ ver | me lho ]'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)

        with self.assertRaises(ParseError):
            parser.parse()



    def test_manual_word_malformed_2(self):
        input   = '[ [ ver me lho ]'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)

        with self.assertRaises(ParseError):
            parser.parse()



    def test_malformed_full_word(self):
        input   = '] ver | me | lho ]'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)

        with self.assertRaises(ParseError):
            parser.parse()


    def test_malformed_stress_all(self):
        input   = 'azul >'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)

        with self.assertRaises(ParseError):
            parser.parse_stress_word()


    def test_malformed_fragment_word(self):
        input   = '| | ver | me | lho |'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)

        with self.assertRaises(ParseError):
            parser.parse()



    def test_verse_phrase_multiple(self):
        input   = '|a|ma|re|lo| e [a|zul] são <minhas sa~udades'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse   = parser.parse()


        self.assertEqual(len(verse.children), 6)

        child_A = verse.children[0]
        self.assertIsInstance(child_A, FragmentWord)
        self.assertEqual(len(child_A.children), 4)

        child_A_1 = child_A.children[0]
        self.assertIsInstance(child_A_1, FragmentString)
        self.assertEqual(len(child_A_1.children), 1)
        self.assertEqual(child_A_1.children[0], String('a'))

        child_A_2 = child_A.children[1]
        self.assertIsInstance(child_A_2, FragmentString)
        self.assertEqual(len(child_A_2.children), 1)
        self.assertEqual(child_A_2.children[0], String('ma'))

        child_A_3 = child_A.children[2]
        self.assertIsInstance(child_A_3, FragmentString)
        self.assertEqual(len(child_A_3.children), 1)
        self.assertEqual(child_A_3.children[0], String('re'))

        child_A_4 = child_A.children[3]
        self.assertIsInstance(child_A_4, FragmentString)
        self.assertEqual(len(child_A_4.children), 1)
        self.assertEqual(child_A_4.children[0], String('lo'))

        child_B = verse.children[1]
        self.assertEqual(child_B, String('e'))

        child_C = verse.children[2]
        self.assertIsInstance(child_C, ManualWord)
        self.assertEqual(len(child_C.children), 2)
        self.assertEqual(child_C.children[0], String('a'))
        self.assertEqual(child_C.children[1], String('zul'))

        child_D = verse.children[3]
        self.assertEqual(child_D, String('são'))

        child_E = verse.children[4]
        self.assertIsInstance(child_E, StressNone)
        self.assertEqual(child_E.children[0], String('minhas'))

        child_F = verse.children[5]
        self.assertIsInstance(child_F, PiecesUntied)
        self.assertEqual(len(child_F.children), 2)
        self.assertEqual(child_F.children[0], String('sa'))
        self.assertEqual(child_F.children[1], String('udades'))



    def test_tied_and_untied_with_fragment_and_manual(self):
        input   = '|la|ran|ja| * e / [a|zul]'
        scanner = VerseScanner(input)
        parser  = VerseParser(scanner)
        verse   = parser.parse()

        self.assertEqual(len(verse.children), 1)

        child_A = verse.children[0]
        self.assertIsInstance(child_A, WordsUntied)
        self.assertEqual(len(child_A.children), 2)
        
        child_A_1 = child_A.children[0]
        self.assertIsInstance(child_A_1, WordsTied)
        self.assertEqual(len(child_A_1.children), 2)

        child_A_1_1 = child_A_1.children[0]
        self.assertIsInstance(child_A_1_1, FragmentWord)
        self.assertEqual(len(child_A_1_1.children), 3)
        child_A_1_1_1 = child_A_1_1.children[0]
        self.assertIsInstance(child_A_1_1_1, FragmentString)
        self.assertEqual(child_A_1_1_1.children[0], String('la'))
        child_A_1_1_2 = child_A_1_1.children[1]
        self.assertIsInstance(child_A_1_1_2, FragmentString)
        self.assertEqual(child_A_1_1_2.children[0], String('ran'))
        child_A_1_1_3 = child_A_1_1.children[2]
        self.assertIsInstance(child_A_1_1_3, FragmentString)
        self.assertEqual(child_A_1_1_3.children[0], String('ja'))

        child_A_1_2 = child_A_1.children[1]
        self.assertEqual(child_A_1_2, String('e'))

        child_A_2 = child_A.children[1]
        self.assertIsInstance(child_A_2, ManualWord)
        self.assertEqual(len(child_A_2.children), 2)
        self.assertEqual(child_A_2.children[0], String('a'))
        self.assertEqual(child_A_2.children[1], String('zul'))
