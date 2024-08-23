import re
from unittest import TestCase
from src.syllables.classes import Syllable



class TestClassSyllable(TestCase):

    def test_properties(self):
        syllable = Syllable()
        self.assertFalse(syllable.has_onset())
        self.assertFalse(syllable.has_nucleus())
        self.assertFalse(syllable.has_coda())
        self.assertFalse(syllable.has_onset_digraph())
        self.assertFalse(syllable.has_onset_cluster())
        self.assertFalse(syllable.has_coda_cluster())
        self.assertFalse(syllable.has_diphthong())
        self.assertFalse(syllable.has_stress())


        syllable_2 = Syllable(onset='v', nucleus='i', coda='r')
        self.assertTrue(syllable_2.has_onset())
        self.assertTrue(syllable_2.has_nucleus())
        self.assertTrue(syllable_2.has_coda())
        self.assertFalse(syllable_2.has_onset_digraph())
        self.assertFalse(syllable_2.has_onset_cluster())
        self.assertFalse(syllable_2.has_coda_cluster())
        self.assertFalse(syllable_2.has_diphthong())
        self.assertFalse(syllable_2.has_stress())

        syllable_3 = Syllable(onset='cr', nucleus='e', coda='r')
        self.assertTrue(syllable_3.has_onset())
        self.assertTrue(syllable_3.has_nucleus())
        self.assertTrue(syllable_3.has_coda())
        self.assertTrue(syllable_3.has_onset_cluster())
        self.assertFalse(syllable_3.has_onset_digraph())
        self.assertFalse(syllable_3.has_coda_cluster())
        self.assertFalse(syllable_3.has_diphthong())
        self.assertFalse(syllable_3.has_stress())

        syllable_5 = Syllable(onset='ss', nucleus='a', coda='r' )
        self.assertTrue(syllable_5.has_onset())
        self.assertTrue(syllable_5.has_nucleus())
        self.assertTrue(syllable_5.has_coda())
        self.assertTrue(syllable_5.has_onset_digraph())
        self.assertFalse(syllable_5.has_onset_cluster())
        self.assertFalse(syllable_5.has_coda_cluster())
        self.assertFalse(syllable_5.has_diphthong())
        self.assertFalse(syllable_5.has_stress())

        syllable_6 = Syllable(onset='s', nucleus='ai', coda='s' )
        self.assertTrue(syllable_6.has_onset())
        self.assertTrue(syllable_6.has_nucleus())
        self.assertTrue(syllable_6.has_coda())
        self.assertTrue(syllable_6.has_diphthong())
        self.assertFalse(syllable_6.has_onset_digraph())
        self.assertFalse(syllable_6.has_onset_cluster())
        self.assertFalse(syllable_6.has_coda_cluster())
        self.assertFalse(syllable_6.has_stress())

        syllable_6 = Syllable(onset='t', nucleus='e', coda='ns' )
        self.assertTrue(syllable_6.has_onset())
        self.assertTrue(syllable_6.has_nucleus())
        self.assertTrue(syllable_6.has_coda())
        self.assertTrue(syllable_6.has_coda_cluster())
        self.assertFalse(syllable_6.has_diphthong())
        self.assertFalse(syllable_6.has_onset_digraph())
        self.assertFalse(syllable_6.has_onset_cluster())
        self.assertFalse(syllable_6.has_stress())

        syllable_7 = Syllable(onset='v', nucleus='a', coda='i', stress=True)
        self.assertTrue(syllable_7.has_onset())
        self.assertTrue(syllable_7.has_nucleus())
        self.assertTrue(syllable_7.has_coda())
        self.assertTrue(syllable_7.has_stress())
        self.assertFalse(syllable_7.has_coda_cluster())
        self.assertFalse(syllable_7.has_diphthong())
        self.assertFalse(syllable_7.has_onset_digraph())
        self.assertFalse(syllable_7.has_onset_cluster())


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
