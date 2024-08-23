from unittest import TestCase
from src.words.splitter import WordSplitter



class TestWordsWithOnset(TestCase):

    def test_cluster_with_rl(self):
        splitter = WordSplitter()

        text = 'abraço'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', '',   'a', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'br', 'a', ''], word.syllables[1].parts())
        self.assertListEqual(['', 'ç',  'o', ''], word.syllables[2].parts())

        text = 'prato'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'pr', 'a', ''], word.syllables[0].parts())
        self.assertListEqual(['', 't',  'o', ''], word.syllables[1].parts())

        text = 'tecla'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 't',  'e', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'cl', 'a', ''], word.syllables[1].parts())




    def test_dipragh(self):
        splitter = WordSplitter()

        text = 'tchéquia'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'tch', 'é', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'qu',  'i', ''], word.syllables[1].parts())
        self.assertListEqual(['', '',    'a', ''], word.syllables[2].parts())

        text = 'velho'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'v',  'e', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'lh', 'o', ''], word.syllables[1].parts())

        text = 'chato'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'ch', 'a', ''], word.syllables[0].parts())
        self.assertListEqual(['', 't',  'o', ''], word.syllables[1].parts())

        text = 'carro'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'c',  'a', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'rr', 'o', ''], word.syllables[1].parts())

        text = 'assado'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', '',   'a', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'ss', 'a', ''], word.syllables[1].parts())
        self.assertListEqual(['', 'd',  'o', ''], word.syllables[2].parts())

        text = 'nhonho'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'nh', 'o', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'nh', 'o', ''], word.syllables[1].parts())

        text = 'guerra'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'gu', 'e', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'rr', 'a', ''], word.syllables[1].parts())

        text = 'leque'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'l',  'e', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'qu', 'e', ''], word.syllables[1].parts())

        text = 'exceto'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', '',   'e', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'xc', 'e', ''], word.syllables[1].parts())
        self.assertListEqual(['', 't',  'o', ''], word.syllables[2].parts())

        text = 'descendente'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', 'd',  'e',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'sc', 'e', 'n'], word.syllables[1].parts())
        self.assertListEqual(['', 'd',  'e', 'n'], word.syllables[2].parts())
        self.assertListEqual(['', 't',  'e',  ''], word.syllables[3].parts())

        text = 'exsurgir'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', '',   'e',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'xs', 'u', 'r'], word.syllables[1].parts())
        self.assertListEqual(['', 'g',  'i', 'r'], word.syllables[2].parts())

        text = 'nasço'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'n',  'a', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'sç', 'o', ''], word.syllables[1].parts())




    def test_cluster_separable_off(self):
        splitter = WordSplitter()

        text = 'friccionar'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', 'fr', 'i',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'cc', 'i',  ''], word.syllables[1].parts())
        self.assertListEqual(['', '',   'o',  ''], word.syllables[2].parts())
        self.assertListEqual(['', 'n',  'a', 'r'], word.syllables[3].parts())

        text = 'convicção'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'c',  'o',  'n'], word.syllables[0].parts())
        self.assertListEqual(['', 'v',  'i',   ''], word.syllables[1].parts())
        self.assertListEqual(['', 'cç', 'ão',  ''], word.syllables[2].parts())

        text = 'compacto'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'c',  'o', 'm'], word.syllables[0].parts())
        self.assertListEqual(['', 'p',  'a',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 'ct', 'o',  ''], word.syllables[2].parts())

        text = 'núpcias'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'n',  'ú',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'pc', 'i',  ''], word.syllables[1].parts())
        self.assertListEqual(['', '',   'a', 's'], word.syllables[2].parts())

        text = 'erupção'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', '',   'e',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'r',  'u',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 'pç', 'ão', ''], word.syllables[2].parts())

        text = 'eucalipto'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', '',   'eu', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'c',  'a',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 'l',  'i',  ''], word.syllables[2].parts())
        self.assertListEqual(['', 'pt', 'o',  ''], word.syllables[3].parts())

        text = 'observar'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', '',   'o',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'bs', 'e', 'r'], word.syllables[1].parts())
        self.assertListEqual(['', 'v',  'a', 'r'], word.syllables[2].parts())

        text = 'admitir'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', '',   'a',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'dm', 'i',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 't',  'i', 'r'], word.syllables[2].parts())

        text = 'advogado'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', '',   'a', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'dv', 'o', ''], word.syllables[1].parts())
        self.assertListEqual(['', 'g',  'a', ''], word.syllables[2].parts())
        self.assertListEqual(['', 'd',  'o', ''], word.syllables[3].parts())

        text = 'ritmo'
        word = splitter.run(text)
        self.assertEqual(2, len(word.syllables))
        self.assertListEqual(['', 'r',  'i', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'tm', 'o', ''], word.syllables[1].parts())

        text = 'ignorar'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', '',   'i',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'gn', 'o',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 'r',  'a', 'r'], word.syllables[2].parts())

        text = 'óbvio'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', '',   'ó', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'bv', 'i', ''], word.syllables[1].parts())
        self.assertListEqual(['', '',   'o', ''], word.syllables[2].parts())

        text = 'psiquiatra'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', 'ps', 'i', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'qu', 'i', ''], word.syllables[1].parts())
        self.assertListEqual(['', '',   'a', ''], word.syllables[2].parts())
        self.assertListEqual(['', 'tr', 'a', ''], word.syllables[3].parts())

        text = 'submarino'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', 's',  'u', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'bm', 'a', ''], word.syllables[1].parts())
        self.assertListEqual(['', 'r',  'i', ''], word.syllables[2].parts())
        self.assertListEqual(['', 'n',  'o', ''], word.syllables[3].parts())

        text = 'tecnologia'
        word = splitter.run(text)
        self.assertEqual(5, len(word.syllables))
        self.assertListEqual(['', 't',  'e', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'cn', 'o', ''], word.syllables[1].parts())
        self.assertListEqual(['', 'l',  'o', ''], word.syllables[2].parts())
        self.assertListEqual(['', 'g',  'i', ''], word.syllables[3].parts())
        self.assertListEqual(['', '',   'a', ''], word.syllables[4].parts())

        text = 'mnemônico'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', 'mn', 'e', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'm',  'ô', ''], word.syllables[1].parts())
        self.assertListEqual(['', 'n',  'i', ''], word.syllables[2].parts())
        self.assertListEqual(['', 'c',  'o', ''], word.syllables[3].parts())




    def test_cluster_separable_on(self):
        splitter = WordSplitter(split_onset_cluster=True)

        text = 'friccionar'
        word = splitter.run(text)
        self.assertEqual(5, len(word.syllables))
        self.assertListEqual(['', 'fr', 'i',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'c',  '',   ''], word.syllables[1].parts())
        self.assertListEqual(['', 'c',  'i',  ''], word.syllables[2].parts())
        self.assertListEqual(['', '',   'o',  ''], word.syllables[3].parts())
        self.assertListEqual(['', 'n',  'a', 'r'], word.syllables[4].parts())

        text = 'convicção'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', 'c',  'o',  'n'], word.syllables[0].parts())
        self.assertListEqual(['', 'v',  'i',   ''], word.syllables[1].parts())
        self.assertListEqual(['', 'c',  '',    ''], word.syllables[2].parts())
        self.assertListEqual(['', 'ç',  'ão',  ''], word.syllables[3].parts())

        text = 'compacto'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', 'c', 'o', 'm'], word.syllables[0].parts())
        self.assertListEqual(['', 'p', 'a',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 'c', '',   ''], word.syllables[2].parts())
        self.assertListEqual(['', 't', 'o',  ''], word.syllables[3].parts())

        text = 'núpcias'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', 'n', 'ú',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'p', '',   ''], word.syllables[1].parts())
        self.assertListEqual(['', 'c', 'i',  ''], word.syllables[2].parts())
        self.assertListEqual(['', '',  'a', 's'], word.syllables[3].parts())

        text = 'erupção'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', '',  'e',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'r', 'u',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 'p', '',   ''], word.syllables[2].parts())
        self.assertListEqual(['', 'ç', 'ão', ''], word.syllables[3].parts())

        text = 'eucalipto'
        word = splitter.run(text)
        self.assertEqual(5, len(word.syllables))
        self.assertListEqual(['', '',  'eu', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'c', 'a',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 'l', 'i',  ''], word.syllables[2].parts())
        self.assertListEqual(['', 'p', '',   ''], word.syllables[3].parts())
        self.assertListEqual(['', 't', 'o',  ''], word.syllables[4].parts())

        text = 'observar'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', '',  'o',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'b', '',   ''], word.syllables[1].parts())
        self.assertListEqual(['', 's', 'e', 'r'], word.syllables[2].parts())
        self.assertListEqual(['', 'v', 'a', 'r'], word.syllables[3].parts())

        text = 'admitir'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', '',  'a',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'd', '',   ''], word.syllables[1].parts())
        self.assertListEqual(['', 'm', 'i',  ''], word.syllables[2].parts())
        self.assertListEqual(['', 't', 'i', 'r'], word.syllables[3].parts())

        text = 'advogado'
        word = splitter.run(text)
        self.assertEqual(5, len(word.syllables))
        self.assertListEqual(['', '',  'a', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'd', '',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 'v', 'o', ''], word.syllables[2].parts())
        self.assertListEqual(['', 'g', 'a', ''], word.syllables[3].parts())
        self.assertListEqual(['', 'd', 'o', ''], word.syllables[4].parts())

        text = 'ritmo'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'r', 'i', ''], word.syllables[0].parts())
        self.assertListEqual(['', 't', '',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 'm', 'o', ''], word.syllables[2].parts())

        text = 'ignorar'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', '',  'i',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'g', '',   ''], word.syllables[1].parts())
        self.assertListEqual(['', 'n', 'o',  ''], word.syllables[2].parts())
        self.assertListEqual(['', 'r', 'a', 'r'], word.syllables[3].parts())

        text = 'óbvio'
        word = splitter.run(text)
        self.assertEqual(4, len(word.syllables))
        self.assertListEqual(['', '',  'ó', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'b', '',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 'v', 'i', ''], word.syllables[2].parts())
        self.assertListEqual(['', '',  'o', ''], word.syllables[3].parts())

        text = 'psiquiatra'
        word = splitter.run(text)
        self.assertEqual(5, len(word.syllables))
        self.assertListEqual(['', 'p',  '',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 's',  'i', ''], word.syllables[1].parts())
        self.assertListEqual(['', 'qu', 'i', ''], word.syllables[2].parts())
        self.assertListEqual(['', '',   'a', ''], word.syllables[3].parts())
        self.assertListEqual(['', 'tr', 'a', ''], word.syllables[4].parts())

        text = 'submarino'
        word = splitter.run(text)
        self.assertEqual(5, len(word.syllables))
        self.assertListEqual(['', 's', 'u', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'b', '',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 'm', 'a', ''], word.syllables[2].parts())
        self.assertListEqual(['', 'r', 'i', ''], word.syllables[3].parts())
        self.assertListEqual(['', 'n', 'o', ''], word.syllables[4].parts())

        text = 'tecnologia'
        word = splitter.run(text)
        self.assertEqual(6, len(word.syllables))
        self.assertListEqual(['', 't', 'e', ''], word.syllables[0].parts())
        self.assertListEqual(['', 'c', '',  ''], word.syllables[1].parts())
        self.assertListEqual(['', 'n', 'o', ''], word.syllables[2].parts())
        self.assertListEqual(['', 'l', 'o', ''], word.syllables[3].parts())
        self.assertListEqual(['', 'g', 'i', ''], word.syllables[4].parts())
        self.assertListEqual(['', '',  'a', ''], word.syllables[5].parts())

        text = 'mnemônico'
        word = splitter.run(text)
        self.assertEqual(5, len(word.syllables))
        self.assertListEqual(['', 'm', '',  ''], word.syllables[0].parts())
        self.assertListEqual(['', 'n', 'e', ''], word.syllables[1].parts())
        self.assertListEqual(['', 'm', 'ô', ''], word.syllables[2].parts())
        self.assertListEqual(['', 'n', 'i', ''], word.syllables[3].parts())
        self.assertListEqual(['', 'c', 'o', ''], word.syllables[4].parts())



    def test_only_onset(self):
        splitter = WordSplitter()

        text = 's'
        word = splitter.run(text)
        self.assertEqual(1, len(word.syllables))
        self.assertListEqual(['', 's',   '',  ''], word.syllables[0].parts())



    def test_special_symbol(self):
        splitter = WordSplitter()

        text = 'minh\'alma'
        word = splitter.run(text)
        self.assertEqual(3, len(word.syllables))
        self.assertListEqual(['', 'm',   'i',  ''], word.syllables[0].parts())
        self.assertListEqual(['', "nh'", 'a', 'l'], word.syllables[1].parts())
        self.assertListEqual(['', 'm',   'a',  ''], word.syllables[2].parts())
