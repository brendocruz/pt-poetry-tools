import re
from unittest import TestCase

from src.syllables.classes import Syllable, PoeticSyllable
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




class TestClassPoeticSyllable(TestCase):

    def test_is_empty_true(self):
        syllable = PoeticSyllable()
        self.assertTrue(syllable.is_empty())



    def test_is_empty_false(self):
        syllable = PoeticSyllable()
        prefix_coda = Syllable(nucleus='a', coda='s')
        syllable.prefix_coda = prefix_coda
        self.assertFalse(syllable.is_empty())

        syllable = PoeticSyllable()
        source = Syllable(nucleus='a')
        syllable.sources.append(source)
        self.assertFalse(syllable.is_empty())



    def test_text_with_prefix(self):
        prefix   = Syllable(nucleus='o', coda='s')
        source_1 = Syllable(nucleus='a')
        source_2 = Syllable(nucleus='a')
        source_3 = Syllable(nucleus='a', coda='s')

        syllable = PoeticSyllable()
        syllable.prefix_coda = prefix
        syllable.sources.append(source_1)
        syllable.sources.append(source_2)
        syllable.sources.append(source_3)

        text = syllable.text(delim='_')
        self.assertEqual(text, 's_a_a_as')



    def test_text_without_prefix(self):
        source_1 = Syllable(nucleus='a')
        source_2 = Syllable(nucleus='a')
        source_3 = Syllable(nucleus='a', coda='s')

        syllable = PoeticSyllable()
        syllable.sources.append(source_1)
        syllable.sources.append(source_2)
        syllable.sources.append(source_3)

        text = syllable.text(delim='_')
        self.assertEqual(text, 'a_a_as')



    def test_has_onset(self):
        syllable = PoeticSyllable()
        prefix   = Syllable(nucleus='o', coda='s')
        syllable.prefix_coda = prefix
        self.assertTrue(syllable.has_onset())

        syllable = PoeticSyllable()
        self.assertFalse(syllable.has_onset())

        syllable = PoeticSyllable()
        source_1 = Syllable(onset='c', nucleus='a')
        source_1.set_props(ONSET, NUCLEUS)
        syllable.sources.append(source_1)
        self.assertTrue(syllable.has_onset())



    def test_has_coda(self):
        syllable = PoeticSyllable()
        self.assertFalse(syllable.has_coda())

        syllable = PoeticSyllable()
        source = Syllable(nucleus='o', coda='s')
        source.set_props(NUCLEUS, CODA)
        syllable.sources.append(source)
        self.assertTrue(syllable.has_coda())



    def test_append(self):
        source_1 = Syllable(onset='m', nucleus='u')
        source_2 = Syllable(nucleus='u')
        source_3 = Syllable(nucleus='u')
        source_4 = Syllable(nucleus='u', coda='h')

        syllable_1 = PoeticSyllable(sources=[source_1, source_2])
        syllable_2 = PoeticSyllable(sources=[source_3, source_4])

        syllable_1.append(syllable_2)
        self.assertEqual(len(syllable_1.sources), 4)
        self.assertEqual(syllable_1.text(delim='_'), 'mu_u_u_uh')
