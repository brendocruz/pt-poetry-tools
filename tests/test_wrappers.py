from unittest import TestCase
from src.syllables import Syllable
from src.words import Word


class TestSyllableClasse(TestCase):
    def test_length_when_empty(self):
        syllable = Syllable()
        self.assertEqual(0, len(syllable))

    def test_length_when_not_empty(self):
        syllable = Syllable()
        syllable.nucleus = 'a'
        self.assertEqual(1, len(syllable))

        syllable = Syllable()
        syllable.onset   = 'c'
        syllable.nucleus = 'a'
        self.assertEqual(2, len(syllable))

        syllable = Syllable()
        syllable.onset   = 'pr'
        syllable.nucleus = 'a'
        syllable.coda    = 'n'
        self.assertEqual(4, len(syllable))

    def test_str_when_empty(self):
        syllable = Syllable()
        self.assertEqual('', syllable.get())

    def test_str_when_not_empty(self):
        syllable = Syllable()
        syllable.nucleus = 'a'
        self.assertEqual('a', syllable.get())

        syllable = Syllable()
        syllable.onset   = 'c'
        syllable.nucleus = 'a'
        self.assertEqual('ca', syllable.get())

        syllable = Syllable()
        syllable.onset   = 'pr'
        syllable.nucleus = 'a'
        syllable.coda    = 'n'
        self.assertEqual('pran', syllable.get())


class TestWordClass(TestCase):
    def test_length_when_empty(self):
        word = Word()
        self.assertEqual(0, len(word))

    def test_length_when_not_empty(self):
        syllables = []

        syllable_1 = Syllable()
        syllable_1.onset = 'b'
        syllable_1.nucleus = 'a'
        syllables.append(syllable_1)

        syllable_2 = Syllable()
        syllable_2.onset = 'n'
        syllable_2.nucleus = 'a'
        syllables.append(syllable_2)

        syllable_3 = Syllable()
        syllable_3.onset = 'n'
        syllable_3.nucleus = 'a'
        syllables.append(syllable_3)

        word = Word(syllables)
        self.assertEqual(6, len(word))

    def test_str_when_empty(self):
        word = Word()
        self.assertEqual('', word.get())

    def test_str_when_not_empty(self):
        syllables = []

        syllable_1 = Syllable()
        syllable_1.onset = 'b'
        syllable_1.nucleus = 'a'
        syllables.append(syllable_1)

        syllable_2 = Syllable()
        syllable_2.onset = 'n'
        syllable_2.nucleus = 'a'
        syllables.append(syllable_2)

        syllable_3 = Syllable()
        syllable_3.onset = 'n'
        syllable_3.nucleus = 'a'
        syllables.append(syllable_3)

        word = Word(syllables)
        self.assertEqual('banana', word.get())

