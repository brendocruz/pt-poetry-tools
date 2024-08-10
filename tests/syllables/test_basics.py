from unittest import TestCase

from src.words.splitter import WordSplitter
from src.syllables.flags import *



class TestBasicWords(TestCase):

    def test_consonant_start_no_accent(self):
        splitter = WordSplitter()

        text = 'figura'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'f', 'i', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'g', 'u', ''], word.syllables[1].parts())
        self.assertListEqual(['', 'r', 'a', ''], word.syllables[2].parts())
        self.assertEqual(word.syllables[0].props, ONSET | NUCLEUS)
        self.assertEqual(word.syllables[1].props, ONSET | NUCLEUS)
        self.assertEqual(word.syllables[2].props, ONSET | NUCLEUS)

        text = 'banana'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'b', 'a', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'n', 'a', ''], word.syllables[1].parts())
        self.assertListEqual(['', 'n', 'a', ''], word.syllables[2].parts())

        text = 'rude'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'r', 'u', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'd', 'e', ''], word.syllables[1].parts())

        text = 'vi'
        word = splitter.run(text)
        self.assertEqual(1, len(word.syllables))
        self.assertListEqual(['', 'v', 'i', ''], word.syllables[0].parts())
    



    def test_vowel_start_no_accent(self):
        splitter = WordSplitter()

        text = 'abacaxi'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', '',  'a', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'b', 'a', ''], word.syllables[1].parts())
        self.assertListEqual(['', 'c', 'a', ''], word.syllables[2].parts())
        self.assertListEqual(['', 'x', 'i', ''], word.syllables[3].parts())
        self.assertEqual(word.syllables[0].props, NUCLEUS)
        self.assertEqual(word.syllables[1].props, ONSET | NUCLEUS)
        self.assertEqual(word.syllables[2].props, ONSET | NUCLEUS)
        self.assertEqual(word.syllables[3].props, ONSET | NUCLEUS)

        text = 'agora'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', '',  'a', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'g', 'o', ''], word.syllables[1].parts())
        self.assertListEqual(['', 'r', 'a', ''], word.syllables[2].parts())

        text = 'ele'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', '',  'e', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'l', 'e', ''], word.syllables[1].parts())

        text = 'a'
        word = splitter.run(text)
        self.assertEqual(1, len(word.syllables))
        self.assertListEqual(['', '', 'a', ''], word.syllables[0].parts())




    def test_consonant_start_and_accent(self):
        splitter = WordSplitter()

        text = 'básico'
        word = splitter.run(text)
        self.assertEqual(3,    len(word.syllables))
        self.assertListEqual(['', 'b', 'á', ''], word.syllables[0].parts())
        self.assertListEqual(['', 's', 'i', ''], word.syllables[1].parts())
        self.assertListEqual(['', 'c', 'o', ''], word.syllables[2].parts())
        self.assertEqual(word.syllables[0].props, ONSET | NUCLEUS)
        self.assertEqual(word.syllables[1].props, ONSET | NUCLEUS)
        self.assertEqual(word.syllables[2].props, ONSET | NUCLEUS)

        text = 'maçã'
        word = splitter.run(text)
        self.assertEqual(2,    len(word.syllables))
        self.assertListEqual(['', 'm', 'a', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'ç', 'ã', ''], word.syllables[1].parts())

        text = 'vê'
        word = splitter.run(text)
        self.assertEqual(1,    len(word.syllables))
        self.assertListEqual(['', 'v', 'ê', ''], word.syllables[0].parts())



    def test_vowel_start_and_accent(self):
        splitter = WordSplitter()

        text = 'átomo'
        word = splitter.run(text)
        self.assertEqual(3,    len(word.syllables))
        self.assertListEqual(['', '',  'á', ''], word.syllables[0].parts())
        self.assertListEqual(['', 't', 'o', ''], word.syllables[1].parts())
        self.assertListEqual(['', 'm', 'o', ''], word.syllables[2].parts())
        self.assertEqual(word.syllables[0].props, NUCLEUS)
        self.assertEqual(word.syllables[1].props, ONSET | NUCLEUS)
        self.assertEqual(word.syllables[2].props, ONSET | NUCLEUS)

        text = 'alô'
        word = splitter.run(text)
        self.assertEqual(2,    len(word.syllables))
        self.assertListEqual(['', '',  'a', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'l', 'ô', ''], word.syllables[1].parts())

        text = 'é'
        word = splitter.run(text)
        self.assertEqual(1,    len(word.syllables))
        self.assertListEqual(['', '', 'é', ''], word.syllables[0].parts())
