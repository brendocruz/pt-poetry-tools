from unittest import TestCase
from src.syllables.classes import Syllable
from src.words.classes import Word



class TestWordClass(TestCase):

    def test_length_when_empty(self):
        word = Word()
        self.assertEqual(0, len(word))



    def test_length_when_not_empty(self):
        syllables  = []
        syllable_1 = Syllable(onset='b', nucleus='a')
        syllable_2 = Syllable(onset='n', nucleus='a')
        syllable_3 = Syllable(onset='n', nucleus='a')
        syllables.extend([syllable_1, syllable_2, syllable_3])

        word = Word(syllables)
        self.assertEqual(6, len(word))



    def test_str_when_empty(self):
        word = Word()
        self.assertEqual('', word.text())



    def test_str_when_not_empty(self):
        syllables  = []
        syllable_1 = Syllable(onset='b', nucleus='a')
        syllable_2 = Syllable(onset='n', nucleus='a')
        syllable_3 = Syllable(onset='n', nucleus='a')
        syllables.extend([syllable_1, syllable_2, syllable_3])

        word = Word(syllables)
        self.assertEqual('banana', word.text())

