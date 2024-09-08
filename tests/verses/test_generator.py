from src.words.splitter import WordSplitter
from src.verses.scanner import VerseScanner
from src.verses.parser import VerseParser
from src.verses.generator import VerseGenerator
from src.stress.finder import StressFinder
from unittest import TestCase


class TestVerseGenerator(TestCase):

    def test_multiple_string(self):
        text      = 'vermelho azul verde'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        self.assertEqual(output, '|ver|+me|lho_a|+zul|+ver|--de|')



    def test_tied_pieces(self):
        text      = 'sa^úde'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        self.assertEqual(output, '|+sa_ú|--de|')



    def test_untied_pieces(self):
        text      = 'o~ito'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        self.assertEqual(output, '|+o|--ito|')



    def test_tied_pieces_merge_error(self):
        text      = 'ver^melho'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        self.assertEqual(output, '|ver|+me|--lho|')



    def test_tied_pieces_twice(self):
        text      = 'po^esi^a'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        self.assertEqual(output, '|po_e|+si_a|')



    def test_untied_pieces_twice(self):
        text      = 'ca~uso~u'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        self.assertEqual(output, '|ca|u|+so|--u|')



    def test_tied_pieces_and_untied_pieces(self):
        text      = 'pro^ibi~u tudo'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        self.assertEqual(output, '|pro_i|+bi|u|+tu|--do|')



    def test_untied_pieces_and_tied_pieces(self):
        text      = 'á~ure^o dia'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        self.assertEqual(output, '|+á|u|re_o|+di|--a|')



    def test_manual_words(self):
        text      = '[ a | ma | re | lo ]'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        self.assertEqual(output, '|a|ma|+re|--lo|')



    def test_all_stressed(self):
        text      = '> amarelo'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        self.assertEqual(output, '|+a|+ma|+re|+lo|')



    def test_all_unstressed(self):
        text      = '< amarelo'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        self.assertEqual(output, '|a|ma|re|lo|')



    def test_fragment_word_stressed(self):
        text      = '|+a|ma|+re|lo|'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        self.assertEqual(output, '|+a|ma|+re|--lo|')


    def test_fragment_word_join(self):
        text      = '|ca|sa_a|zul|'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        self.assertEqual(output, '|ca|sa_a|zul|')



    def test_all(self):
        text      = '|+tris|te|+di_a| <meu gato [cin|za] está |mo|no|si|+lá|--bico|'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        desired   = '|+tris|te|+di_a|meu|+ga|to|+cin|za_es|+tá|mo|no|si|+lá|--bico|'
        self.assertEqual(desired, output)



    def test_merge_syllables_dipthong_hiatus(self):
        text      = 'sei o seu segredo'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        desired   = '|+sei|o|+seu|se|+gre|--do|'
        self.assertEqual(desired, output)


    def test_merge_syllables_hiatus_diphthong(self):
        text      = 'estreou o vestido novo'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        desired   = '|es|tre|+ou|o|ves|+ti|do|+no|--vo|'
        self.assertEqual(desired, output)


    def test_merge_syllables_left_multiple_sources(self):
        text      = 'mei^o a meio'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        desired   = '|+mei_o|a|+mei|--o|'
        self.assertEqual(desired, output)


    def test_merge_syllables_right_before_end(self):
        text      = 'ele me amou'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        desired   = '|+e|le|me_a|+mou|'
        self.assertEqual(desired, output)



    def test_merge_syllables_prefix_simple(self):
        text      = 'mais um dia'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        desired   = '|+mai|s_um|+di|--a|'
        self.assertEqual(desired, output)



    def test_merge_syllables_coda_prefix_complex(self):
        text      = 'tens o amor'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        desired   = '|+ten|s_o_a|+mor|'
        self.assertEqual(desired, output)



    def test_parse_coda_prefix_simple(self):
        text      = '|+mai|s_um|+di|--a|'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        desired   = '|+mai|s_um|+di|--a|'
        self.assertEqual(desired, output)



    def test_parse_coda_prefix_complex(self):
        text      = '|+ten|s_o_a|+mor|'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        desired   = '|+ten|s_o_a|+mor|'
        self.assertEqual(desired, output)



    def test_words_untied(self):
        text      = 'amarelo / azul'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        desired   = '|a|ma|+re|lo|a|+zul|'
        self.assertEqual(desired, output)


    def test_words_tied(self):
        text      = 'amarelo * azul'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        desired   = '|a|ma|+re|lo_a|+zul|'
        self.assertEqual(desired, output)


    def test_words_tied_and_untied(self):
        text      = '|la|ran|ja| * e / [a|zul]'
        splitter  = WordSplitter()
        finder    = StressFinder()
        scanner   = VerseScanner(text)
        parser    = VerseParser(scanner)
        verse     = parser.parse()
        generator = VerseGenerator(splitter, finder)
        output    = generator.run(verse)

        desired   = '|la|ran|ja_e|a|+zul|'
        self.assertEqual(desired, output)
