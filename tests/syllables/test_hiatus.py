from unittest import TestCase
from src.words.splitter import WordSplitter



class TestWordsWithHiatus(TestCase):

    def test_end_with_accented_i(self):
        splitter = WordSplitter()

        text = 'paraíso'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', 'p', 'a', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'r', 'a', ''], word.syllables[1].parts())
        self.assertListEqual(['', '',  'í', ''], word.syllables[2].parts())
        self.assertListEqual(['', 's', 'o', ''], word.syllables[3].parts())

        text = 'cafeína'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', 'c', 'a',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'f', 'e',  ''], word.syllables[1].parts())
        self.assertListEqual(['', '',  'í',  ''], word.syllables[2].parts())
        self.assertListEqual(['', 'n', 'a',  ''], word.syllables[3].parts())

        text = 'egoísmo'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', '',  'e',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'g', 'o',  ''], word.syllables[1].parts())
        self.assertListEqual(['', '',  'í', 's'], word.syllables[2].parts())
        self.assertListEqual(['', 'm', 'o',  ''], word.syllables[3].parts())

        text = 'juízes'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'j', 'u',  ''], word.syllables[0].parts())
        self.assertListEqual(['', '',  'í',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 'z', 'e', 's'], word.syllables[2].parts())




    def test_end_with_accented_u(self):
        splitter = WordSplitter()

        text = 'alaúde'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', '',  'a', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'l', 'a', ''], word.syllables[1].parts())
        self.assertListEqual(['', '',  'ú', ''], word.syllables[2].parts())
        self.assertListEqual(['', 'd', 'e', ''], word.syllables[3].parts())

        text = 'ciúme'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'c', 'i', ''], word.syllables[0].parts())
        self.assertListEqual(['', '',  'ú', ''], word.syllables[1].parts())
        self.assertListEqual(['', 'm', 'e', ''], word.syllables[2].parts())




    def test_before_consonant_on_word_end(self):
        splitter = WordSplitter()

        text = 'adail'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', '',  'a',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'd', 'a',  ''], word.syllables[1].parts())
        self.assertListEqual(['', '',  'i', 'l'], word.syllables[2].parts())

        text = 'ruim'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'r',  'u',  ''], word.syllables[0].parts())
        self.assertListEqual(['', '',   'i', 'm'], word.syllables[1].parts())

        text = 'juiz'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'j',  'u',  ''], word.syllables[0].parts())
        self.assertListEqual(['', '',   'i', 'z'], word.syllables[1].parts())

        text = 'influir'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', '',   'i', 'n'], word.syllables[0].parts())
        self.assertListEqual(['', 'fl', 'u',  ''], word.syllables[1].parts())
        self.assertListEqual(['', '',   'i', 'r'], word.syllables[2].parts())




    def test_before_cluster(self):
        splitter = WordSplitter()

        text = 'rainha'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'r',  'a', ''], word.syllables[0].parts())
        self.assertListEqual(['', '',   'i', ''], word.syllables[1].parts())
        self.assertListEqual(['', 'nh', 'a', ''], word.syllables[2].parts())

        text = 'coimbra'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'c',  'o',  ''], word.syllables[0].parts())
        self.assertListEqual(['', '',   'i', 'm'], word.syllables[1].parts())
        self.assertListEqual(['', 'br', 'a',  ''], word.syllables[2].parts())

        text = 'ainda'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', '',  'a',  ''], word.syllables[0].parts())
        self.assertListEqual(['', '',  'i', 'n'], word.syllables[1].parts())
        self.assertListEqual(['', 'd', 'a',  ''], word.syllables[2].parts())

        text = 'triunfo'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'tr', 'i',  ''], word.syllables[0].parts())
        self.assertListEqual(['', '',   'u', 'n'], word.syllables[1].parts())
        self.assertListEqual(['', 'f',  'o',  ''], word.syllables[2].parts())

        text = 'influirmos'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', '',   'i', 'n'], word.syllables[0].parts())
        self.assertListEqual(['', 'fl', 'u',  ''], word.syllables[1].parts())
        self.assertListEqual(['', '',   'i', 'r'], word.syllables[2].parts())
        self.assertListEqual(['', 'm',  'o', 's'], word.syllables[3].parts())



    def test_hiatus_always(self):
        splitter = WordSplitter()

        text = 'realizar'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', 'r', 'e',  ''], word.syllables[0].parts())
        self.assertListEqual(['', '',  'a',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 'l', 'i',  ''], word.syllables[2].parts())
        self.assertListEqual(['', 'z', 'a', 'r'], word.syllables[3].parts())

        text = 'vídeo'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'v', 'í', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'd', 'e', ''], word.syllables[1].parts())
        self.assertListEqual(['', '',  'o', ''], word.syllables[2].parts())

        text = 'calúnia'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', 'c', 'a', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'l', 'ú', ''], word.syllables[1].parts())
        self.assertListEqual(['', 'n', 'i', ''], word.syllables[2].parts())
        self.assertListEqual(['', '',  'a', ''], word.syllables[3].parts())

        text = 'espécie'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', '',  'e', 's'], word.syllables[0].parts())
        self.assertListEqual(['', 'p', 'é',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 'c', 'i',  ''], word.syllables[2].parts())
        self.assertListEqual(['', '',  'e',  ''], word.syllables[3].parts())

        text = 'ocioso'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', '',  'o', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'c', 'i', ''], word.syllables[1].parts())
        self.assertListEqual(['', '',  'o', ''], word.syllables[2].parts())
        self.assertListEqual(['', 's', 'o', ''], word.syllables[3].parts())

        text = 'mágoa'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'm', 'á', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'g', 'o', ''], word.syllables[1].parts())
        self.assertListEqual(['', '',  'a', ''], word.syllables[2].parts())

        text = 'mútua'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'm', 'ú', ''], word.syllables[0].parts())
        self.assertListEqual(['', 't', 'u', ''], word.syllables[1].parts())
        self.assertListEqual(['', '',  'a', ''], word.syllables[2].parts())

        text = 'cruel'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'cr', 'u',  ''], word.syllables[0].parts())
        self.assertListEqual(['', '',   'e', 'l'], word.syllables[1].parts())

        text = 'vácuo'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'v', 'á', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'c', 'u', ''], word.syllables[1].parts())
        self.assertListEqual(['', '',  'o', ''], word.syllables[2].parts())


    def test_same_vowel_twice(self):
        splitter = WordSplitter()

        text = 'caatinga'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', 'c', 'a',  ''], word.syllables[0].parts())
        self.assertListEqual(['', '',  'a',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 't', 'i', 'n'], word.syllables[2].parts())
        self.assertListEqual(['', 'g', 'a',  ''], word.syllables[3].parts())
