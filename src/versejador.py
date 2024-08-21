import sys
import os
import argparse

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), './../'))
from src.verses.scanner import VerseScanner
from src.verses.parser import VerseParser
from src.verses.generator import VerseGenerator
from src.words.splitter import WordSplitter
from src.stress.finder import StressFinder

help_verse = 'O verso que será metrificado.'
help_help  = 'Mostra essa mensagem e sai.'

argparser = argparse.ArgumentParser(description='', add_help=False)
argparser.add_argument('verse', type=str, help=help_verse)
argparser.add_argument('-h', '--help', action='help', help=help_help)


def main():
    args = argparser.parse_args()

    scanner   = VerseScanner(args.verse)
    parser    = VerseParser(scanner)
    splitter  = WordSplitter()
    finder    = StressFinder()
    generator = VerseGenerator(splitter, finder)
    verse     = parser.parse()
    output    = generator.run(verse)
    print(output)


if __name__ == '__main__':
    main()
