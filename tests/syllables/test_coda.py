from unittest import TestCase
from src.syllables.flags import *
from src.words.splitter import WordSplitter



class TestWordsWithCoda(TestCase):

    def test_basic(self):
        splitter = WordSplitter()

        text = 'fazer'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'f', 'a',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'z', 'e', 'r'], word.syllables[1].parts())
        self.assertEqual(word.syllables[0].props, ONSET | NUCLEUS)
        self.assertEqual(word.syllables[1].props, ONSET | NUCLEUS | CODA)

        text = 'certo'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'c', 'e', 'r'], word.syllables[0].parts())
        self.assertListEqual(['', 't', 'o',  ''], word.syllables[1].parts())

        text = 'sal'
        word = splitter.run(text)
        self.assertEqual(1, len(word.syllables))
        self.assertListEqual(['', 's', 'a', 'l'], word.syllables[0].parts())

        text = 'ah'
        word = splitter.run(text)
        self.assertEqual(1, len(word.syllables))
        self.assertListEqual(['', '', 'a', 'h'], word.syllables[0].parts())




    def test_digraph_sometimes(self):
        splitter = WordSplitter()

        text = 'excarcerar'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', '',  'e', 'x'], word.syllables[0].parts())
        self.assertListEqual(['', 'c', 'a', 'r'], word.syllables[1].parts())
        self.assertListEqual(['', 'c', 'e',  ''], word.syllables[2].parts())
        self.assertListEqual(['', 'r', 'a', 'r'], word.syllables[3].parts())
        self.assertEqual(word.syllables[0].props, NUCLEUS | CODA)
        self.assertEqual(word.syllables[1].props, ONSET | NUCLEUS | CODA)
        self.assertEqual(word.syllables[2].props, ONSET | NUCLEUS)
        self.assertEqual(word.syllables[3].props, ONSET | NUCLEUS | CODA)

        text = 'excluir'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', '',   'e', 'x'], word.syllables[0].parts())
        self.assertListEqual(['', 'cl', 'u',  ''], word.syllables[1].parts())
        self.assertListEqual(['', '',   'i', 'r'], word.syllables[2].parts())

        text = 'pescar'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'p', 'e', 's'], word.syllables[0].parts())
        self.assertListEqual(['', 'c', 'a', 'r'], word.syllables[1].parts())

        text = 'consigo'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'c', 'o', 'n'], word.syllables[0].parts())
        self.assertListEqual(['', 's', 'i',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 'g', 'o',  ''], word.syllables[2].parts())




    def test_cluster_middle(self):
        splitter = WordSplitter()

        text = 'transporte'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'tr', 'a', 'ns'], word.syllables[0].parts())
        self.assertListEqual(['', 'p',  'o',  'r'], word.syllables[1].parts())
        self.assertListEqual(['', 't',  'e',   ''], word.syllables[2].parts())
        self.assertEqual(word.syllables[0].props, 
                         ONSET | NUCLEUS | CODA | CODA_CLUSTER | ONSET_CLUSTER)
        self.assertEqual(word.syllables[1].props, ONSET | NUCLEUS | CODA)
        self.assertEqual(word.syllables[2].props, ONSET | NUCLEUS)




    def test_cluster_end(self):
        splitter = WordSplitter()

        text = 'bíceps'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'b', 'í',   ''], word.syllables[0].parts())
        self.assertListEqual(['', 'c', 'e', 'ps'], word.syllables[1].parts())
        self.assertEqual(word.syllables[0].props, ONSET | NUCLEUS)
        self.assertEqual(word.syllables[1].props, ONSET | NUCLEUS | CODA | CODA_CLUSTER)

        text = 'hífens'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'h', 'í',   ''], word.syllables[0].parts())
        self.assertListEqual(['', 'f', 'e', 'ns'], word.syllables[1].parts())
