import re
from unittest import TestCase
from src.syllables.classes import Syllable
from src.syllables.flags import ONSET, CODA, NUCLEUS



class TestClassSyllable(TestCase):

    def test_props(self):
        syllable = Syllable()
        self.assertEqual(syllable.props, 0)

        syllable.set_props(ONSET, CODA)
        self.assertEqual(syllable.props, ONSET | CODA)

        result = syllable.has(ONSET)
        self.assertTrue(result)

        result = syllable.has(ONSET, CODA)
        self.assertTrue(result)

        result = syllable.has(NUCLEUS)
        self.assertFalse(result)

        result = syllable.has(ONSET, NUCLEUS)
        self.assertFalse(result)

        result = syllable.has(NUCLEUS, CODA)
        self.assertFalse(result)


    def test_text(self):
        syllable = Syllable(onset='gr', nucleus='a', coda='n')
        self.assertEqual(syllable.text(), 'gran')

        syllable = Syllable(onset='d', nucleus='e')
        self.assertEqual(syllable.text(), 'de')

        syllable = Syllable(nucleus='aí')
        self.assertEqual(syllable.text(), 'aí')


    def test_parts(self):
        syllable = Syllable(onset='gr', nucleus='a', coda='n')
        self.assertListEqual(syllable.parts(), ['', 'gr', 'a', 'n'])

        syllable = Syllable(onset='d', nucleus='e')
        self.assertListEqual(syllable.parts(), ['', 'd', 'e', ''])

        syllable = Syllable(nucleus='aí')
        self.assertListEqual(syllable.parts(), ['', '', 'aí', ''])



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
        self.assertEqual('', syllable.text())



    def test_str_when_not_empty(self):
        syllable = Syllable()
        syllable.nucleus = 'a'
        self.assertEqual('a', syllable.text())

        syllable = Syllable()
        syllable.onset   = 'c'
        syllable.nucleus = 'a'
        self.assertEqual('ca', syllable.text())

        syllable = Syllable()
        syllable.onset   = 'pr'
        syllable.nucleus = 'a'
        syllable.coda    = 'n'
        self.assertEqual('pran', syllable.text())



    def test_repr(self):
        syllable = Syllable(onset='s', nucleus='e', coda='r')
        syllable.set_props(ONSET, NUCLEUS, CODA)
        pattern = re.compile('^<.+>$')
        self.assertNotRegex(repr(syllable), pattern)


    def test_merge(self):
        syllable_1 = Syllable(prefix='-', onset='m', nucleus='e', coda='')
        syllable_2 = Syllable(prefix='',  onset='',  nucleus='u', coda='s')
        syllable_3 = syllable_1.merge(syllable_2)

        assert isinstance(syllable_3, Syllable)
        self.assertEqual(syllable_3.text(), '-meus')
        self.assertListEqual(syllable_3.parts(), ['-', 'm', 'eu', 's'])


        syllable_1 = Syllable(prefix='',  onset='l', nucleus='o',  coda='')
        syllable_2 = Syllable(prefix='-', onset='',  nucleus='ei', coda='')
        syllable_3 = syllable_1.merge(syllable_2)
        self.assertIsNone(syllable_3)

        syllable_1 = Syllable(prefix='', onset='t', nucleus='o', coda='')
        syllable_2 = Syllable(prefix='', onset='d', nucleus='e', coda='')
        syllable_3 = syllable_1.merge(syllable_2)
        self.assertIsNone(syllable_3)

        syllable_1 = Syllable(prefix='', onset='t', nucleus='o', coda='s')
        syllable_2 = Syllable(prefix='', onset='d', nucleus='e', coda='')
        syllable_3 = syllable_1.merge(syllable_2)
        self.assertIsNone(syllable_3)
