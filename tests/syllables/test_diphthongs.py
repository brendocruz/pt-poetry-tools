from unittest import TestCase
from src.words.splitter import WordSplitter
from src.syllables.flags import *



class TestWordsWithDiphthongs(TestCase):

    def test_dipthong_always(self):
        splitter = WordSplitter()

        text = 'coração'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'c', 'o',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'r', 'a',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 'ç', 'ão', ''], word.syllables[2].parts())
        self.assertEqual(word.syllables[2].props, ONSET | NUCLEUS | DIPHTHONG)

        text = 'ações'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', '',  'a',   ''], word.syllables[0].parts())
        self.assertListEqual(['', 'ç', 'õe', 's'], word.syllables[1].parts())
        self.assertEqual(word.syllables[1].props, ONSET | NUCLEUS | CODA | DIPHTHONG)

        text = 'cãibra'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'c',  'ãi', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'br', 'a',  ''], word.syllables[1].parts())
        self.assertEqual(word.syllables[0].props, ONSET | NUCLEUS | DIPHTHONG)

        text = 'câimbra'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'c',  'âi', 'm'], word.syllables[0].parts())
        self.assertListEqual(['', 'br', 'a',   ''], word.syllables[1].parts())
        self.assertEqual(word.syllables[0].props, ONSET | NUCLEUS | CODA | DIPHTHONG)

        text = 'mãe'
        word = splitter.run(text)
        self.assertEqual(1, len(word.syllables))
        self.assertListEqual(['', 'm', 'ãe', ''], word.syllables[0].parts())
        self.assertEqual(word.syllables[0].props, ONSET | NUCLEUS | DIPHTHONG)

        text = 'náilon'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'n', 'ái',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'l', 'o',  'n'], word.syllables[1].parts())
        self.assertEqual(word.syllables[0].props, ONSET | NUCLEUS | DIPHTHONG)

        text = 'áureo'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', '',  'áu', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'r', 'e',  ''], word.syllables[1].parts())
        self.assertListEqual(['', '',  'o',  ''], word.syllables[2].parts())
        self.assertEqual(word.syllables[0].props, NUCLEUS | DIPHTHONG)

        text = 'hotéis'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'h', 'o',   ''], word.syllables[0].parts())
        self.assertListEqual(['', 't', 'éi', 's'], word.syllables[1].parts())
        self.assertEqual(word.syllables[1].props, ONSET | NUCLEUS | CODA | DIPHTHONG)

        text = 'contêiner'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'c', 'o',  'n'], word.syllables[0].parts())
        self.assertListEqual(['', 't', 'êi',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 'n', 'e',  'r'], word.syllables[2].parts())
        self.assertEqual(word.syllables[1].props, ONSET | NUCLEUS | DIPHTHONG)

        text = 'chapéu'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'ch', 'a',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'p',  'éu', ''], word.syllables[1].parts())
        self.assertEqual(word.syllables[1].props, ONSET | NUCLEUS | DIPHTHONG)

        text = 'nêutron'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'n',  'êu',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'tr', 'o',  'n'], word.syllables[1].parts())
        self.assertEqual(word.syllables[0].props, ONSET | NUCLEUS | DIPHTHONG)

        text = 'herói'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'h', 'e',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'r', 'ói', ''], word.syllables[1].parts())
        self.assertEqual(word.syllables[1].props, ONSET | NUCLEUS | DIPHTHONG)
