from unittest import TestCase
from src.syllables.classes import Syllable, PoeticSyllable
from src.syllables.flags import ONSET, CODA, NUCLEUS, STRESS



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



    def test_text_with_stress_prefix(self):
        prefix   = Syllable(nucleus='a', coda='s')
        source_1 = Syllable(nucleus='a')
        source_2 = Syllable(nucleus='a')
        source_3 = Syllable(nucleus='a', coda='s', props=STRESS)
        sources  = [source_1, source_2, source_3]
        syllable = PoeticSyllable(sources=sources, prefix_coda=prefix)

        text = syllable.text(delim='_', stress_prefix='+')
        self.assertEqual(text, '+s_a_a_as')



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


    def test_add_prefix(self):
        prefix   = Syllable(onset='d', nucleus='o', coda='s')
        source_2 = Syllable(onset='',  nucleus='ou')
        sources  = [source_2]
        syllable = PoeticSyllable(sources=sources)
        syllable.add_prefix(prefix)
        self.assertEqual(syllable.prefix_coda, prefix)



    def test_append(self):
        source_1 = Syllable(onset='m', nucleus='u')
        source_2 = Syllable(nucleus='u')
        source_3 = Syllable(nucleus='u')
        source_4 = Syllable(nucleus='u', coda='h', props=STRESS)

        syllable = PoeticSyllable(sources=[source_1, source_2])

        syllable.append(source_3)
        syllable.append(source_4)
        self.assertEqual(len(syllable.sources), 4)
        self.assertEqual(syllable.text(delim='_'), 'mu_u_u_uh')
        self.assertTrue(syllable.stress)



    def test_extend(self):
        source_1 = Syllable(onset='m', nucleus='u')
        source_2 = Syllable(nucleus='u')
        source_3 = Syllable(nucleus='u')
        source_4 = Syllable(nucleus='u', coda='h', props=STRESS)

        syllable_1 = PoeticSyllable(sources=[source_1, source_2])
        syllable_2 = PoeticSyllable(sources=[source_3, source_4])

        syllable_1.extend(syllable_2)
        self.assertEqual(len(syllable_1.sources), 4)
        self.assertEqual(syllable_1.text(delim='_'), 'mu_u_u_uh')
        self.assertTrue(syllable_1.stress)
