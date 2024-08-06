from unittest import TestCase
from src.words import WordSplitter
from src.stress import StressFinder



class TestWordsWithOnset(TestCase):
    def test_proparoxytones_accent(self):
        finder = StressFinder()
        splitter = WordSplitter()

        word = splitter.run('matemática')
        index = finder.run(word)
        self.assertEqual(2, index)

        word = splitter.run('abóbora')
        index = finder.run(word)
        self.assertEqual(1, index)

        word = splitter.run('átomo')
        index = finder.run(word)
        self.assertEqual(0, index)




    def test_paroxytones_accent(self):
        finder = StressFinder()
        splitter = WordSplitter()

        word = splitter.run('amável')
        index = finder.run(word)
        self.assertEqual(1, index)

        word = splitter.run('dócil')
        index = finder.run(word)
        self.assertEqual(0, index)




    def test_oxytones_accent(self):
        finder = StressFinder()
        splitter = WordSplitter()

        word = splitter.run('só')
        index = finder.run(word)
        self.assertEqual(0, index)

        word = splitter.run('bebê')
        index = finder.run(word)
        self.assertEqual(1, index)

        word = splitter.run('português')
        index = finder.run(word)
        self.assertEqual(2, index)


    def test_paroxytones_no_accent(self):
        finder = StressFinder()
        splitter = WordSplitter()

        word = splitter.run('gato')
        index = finder.run(word)
        self.assertEqual(0, index)

        word = splitter.run('prolixo')
        index = finder.run(word)
        self.assertEqual(1, index)

        word = splitter.run('talarico')
        index = finder.run(word)
        self.assertEqual(2, index)

        word = splitter.run('dissimulado')
        index = finder.run(word)
        self.assertEqual(3, index)


    def test_oxytones_no_accent(self):
        finder = StressFinder()
        splitter = WordSplitter()

        word = splitter.run('hostil')
        index = finder.run(word)
        self.assertEqual(1, index)

        word = splitter.run('amar')
        index = finder.run(word)
        self.assertEqual(1, index)

        word = splitter.run('talismã')
        index = finder.run(word)
        self.assertEqual(2, index)

        word = splitter.run('irmãs')
        index = finder.run(word)
        self.assertEqual(1, index)

        word = splitter.run('gratidão')
        index = finder.run(word)
        self.assertEqual(2, index)

        word = splitter.run('anciãos')
        index = finder.run(word)
        self.assertEqual(2, index)

        word = splitter.run('jejum')
        index = finder.run(word)
        self.assertEqual(1, index)

        word = splitter.run('incomuns')
        index = finder.run(word)
        self.assertEqual(2, index)

        word = splitter.run('tatus')
        index = finder.run(word)
        self.assertEqual(1, index)

        word = splitter.run('abacaxi')
        index = finder.run(word)
        self.assertEqual(3, index)

        word = splitter.run('caquis')
        index = finder.run(word)
        self.assertEqual(1, index)

        word = splitter.run('farei')
        index = finder.run(word)
        self.assertEqual(1, index)

        word = splitter.run('podeis')
        index = finder.run(word)
        self.assertEqual(1, index)
