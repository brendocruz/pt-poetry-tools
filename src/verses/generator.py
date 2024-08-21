from typing import cast

from src.verses.nodes import *
from src.words.classes import Word
from src.syllables.classes import PoeticSyllable, Syllable
from src.words.splitter import WordSplitter
from src.stress.finder import StressFinder
from src.syllables.flags import STRESS


class VerseGenerator:
    splitter: WordSplitter
    finder: StressFinder

    def __init__(self, splitter: WordSplitter, finder: StressFinder):
        self.splitter = splitter
        self.finder = finder



    def generate_untied_pieces(self, pieces: PiecesUntied) -> list[Syllable]:
        assert len(pieces.children) == 2

        all_syllables: list[list[Syllable]] = []
        for child in pieces.children:
            if isinstance(child, String):
                syllables = self.split_string(child)
                all_syllables.append(syllables)
                continue
            if isinstance(child, PiecesTied):
                syllables = self.generate_tied_pieces(child)
                all_syllables.append(syllables)
                continue
            if isinstance(child, PiecesUntied):
                syllables = self.generate_untied_pieces(child)
                all_syllables.append(syllables)
                continue

        left_piece  = all_syllables[0]
        right_piece = all_syllables[1]

        joined_pieces: list[Syllable] = []
        joined_pieces.extend(left_piece)
        joined_pieces.extend(right_piece)
        return joined_pieces



    def generate_tied_pieces(self, pieces: PiecesTied) -> list[Syllable]:
        assert len(pieces.children) == 2

        all_syllables: list[list[Syllable]] = []
        for child in pieces.children:
            if isinstance(child, String):
                syllables = self.split_string(child)
                all_syllables.append(syllables)
                continue
            if isinstance(child, PiecesTied):
                syllables = self.generate_tied_pieces(child)
                all_syllables.append(syllables)
                continue
            if isinstance(child, PiecesUntied):
                syllables = self.generate_untied_pieces(child)
                all_syllables.append(syllables)
                continue

        left_piece  = all_syllables[0]
        right_piece = all_syllables[1]
        left_edge   = left_piece.pop(-1)
        right_edge  = right_piece.pop(0)

        merged_syllable = left_edge.merge(right_edge)

        if not merged_syllable:
            joined_pieces: list[Syllable] = []
            joined_pieces.extend(left_piece)
            joined_pieces.append(left_edge)
            joined_pieces.append(right_edge)
            joined_pieces.extend(right_piece)
            return joined_pieces

        joined_pieces: list[Syllable] = []
        joined_pieces.extend(left_piece)
        joined_pieces.append(merged_syllable)
        joined_pieces.extend(right_piece)
        return joined_pieces



    def generate_auto_word(self, auto_word: Phrase) -> list[PoeticSyllable]:
        all_syllables: list[Syllable] = []

        if isinstance(auto_word, PiecesTied):
            all_syllables = self.generate_tied_pieces(auto_word)
        elif isinstance(auto_word, PiecesUntied):
            all_syllables = self.generate_untied_pieces(auto_word)


        merged_word  = Word(all_syllables)
        regular_word = self.splitter.run(merged_word.text())
        stress_index = self.finder.run(regular_word)


        # Checa se a palavra é átona.
        # if stress_index == -1:
        #     return merged_word.syllables

        start, end = regular_word.span_text(stress_index)
        indices    = merged_word.span_syllable(start, end)
        choose     = indices[0]
        merged_word.syllables[choose].set_props(STRESS)


        poetic_syllables: list[PoeticSyllable] = []
        for syllable in merged_word.syllables:
            poetic_syllable = PoeticSyllable(sources=[syllable])
            poetic_syllables.append(poetic_syllable)
        return poetic_syllables



    def generate_manual_word(self, manual_word: ManualWord) -> list[PoeticSyllable]:
        all_syllables: list[Syllable] = []
        for piece in manual_word.children:
            if isinstance(piece, String):
                syllables = self.split_string(piece)
                all_syllables.extend(syllables)
        syllables = self.stress_string(all_syllables)

        poetic_syllables: list[PoeticSyllable] = []
        for syllable in syllables:
            poetic_syllable = PoeticSyllable(sources=[syllable])
            poetic_syllables.append(poetic_syllable)
        return poetic_syllables



    def split_and_stress_string(self, string: String) -> list[Syllable]:
        word = self.splitter.run(string.value)
        self.finder.run(word)
        return word.syllables


    def split_string(self, string: String) -> list[Syllable]:
        word = self.splitter.run(string.value)
        return word.syllables


    def stress_string(self, syllables: list[Syllable]) -> list[Syllable]:
        word = Word(syllables)
        self.finder.run(word)
        return word.syllables


    def generate_string(self, string: String) -> list[PoeticSyllable]:
        syllables = self.split_and_stress_string(string)
        poetic_syllables: list[PoeticSyllable] = []
        for syllable in syllables:
            poetic_syllable = PoeticSyllable(sources=[syllable])
            poetic_syllables.append(poetic_syllable)
        return poetic_syllables



    def generate_all_stressed(self, all_stressed: StressAll) -> list[PoeticSyllable]:
        string = all_stressed.children[0]
        string = cast(String, string)
        syllables = self.split_string(string)
        for syllable in syllables:
            syllable.set_props(STRESS)

        poetic_syllables: list[PoeticSyllable] = []
        for syllable in syllables:
            poetic_syllable = PoeticSyllable(sources=[syllable])
            poetic_syllables.append(poetic_syllable)
        return poetic_syllables



    def generate_all_unstressed(self, all_unstressed: StressNone) -> list[PoeticSyllable]:
        string = all_unstressed.children[0]
        string = cast(String, string)
        syllables = self.split_string(string)

        poetic_syllables: list[PoeticSyllable] = []
        for syllable in syllables:
            poetic_syllable = PoeticSyllable(sources=[syllable])
            poetic_syllables.append(poetic_syllable)
        return poetic_syllables



    def generate_fragment_stressed(self, string: FragmentStressed) -> list[PoeticSyllable]:
        fragment  = string.children[0]

        poetic_syllables: list[PoeticSyllable] = []
        if isinstance(fragment, FragmentString):
            poetic_syllables = self.generate_fragment_string(fragment)
        if isinstance(fragment, FragmentJoin):
            poetic_syllables = self.generate_fragment_join(fragment)

        for syllable in poetic_syllables:
            syllable.stress = True
        return poetic_syllables



    def generate_fragment_string(self, fragment: FragmentString) -> list[PoeticSyllable]:
        string    = fragment.children[0]
        string    = cast(String, string)
        syllables = self.split_string(string)

        poetic_syllables: list[PoeticSyllable] = []
        for syllable in syllables:
            poetic_syllable = PoeticSyllable(sources=[syllable])
            poetic_syllables.append(poetic_syllable)
        return poetic_syllables



    def generate_fragment_join(self, fragment: FragmentJoin) -> list[PoeticSyllable]:
        poetic_syllable = PoeticSyllable()
        for child in fragment.children:
            child = cast(String, child)
            syllables = self.split_string(child)
            other = PoeticSyllable(sources=syllables)
            poetic_syllable.extend(other)
        return [poetic_syllable]



    def generate_fragment_rest(self, fragment: FragmentRest) -> list[PoeticSyllable]:
        string = fragment.children[0]
        string = cast(String, string)
        syllables = self.split_string(string)

        poetic_syllable = PoeticSyllable()
        for syllable in syllables:
            poetic_syllable.append(syllable)
        return [poetic_syllable]




    def generate_fragment_word(self, fragment_word: FragmentWord) -> list[PoeticSyllable]:
        poetic_syllables: list[PoeticSyllable] = []
        for child in fragment_word.children:
            if isinstance(child, FragmentString):
                syllables = self.generate_fragment_string(child)
                poetic_syllables.extend(syllables)
                continue
            if isinstance(child, FragmentJoin):
                syllables = self.generate_fragment_join(child)
                poetic_syllables.extend(syllables)
                continue
            if isinstance(child, FragmentStressed):
                syllables = self.generate_fragment_stressed(child)
                poetic_syllables.extend(syllables)
                continue
            if isinstance(child, FragmentRest):
                syllables = self.generate_fragment_rest(child)
                poetic_syllables.extend(syllables)
                continue
        return poetic_syllables



    def generate_verse(self, verse: Verse) -> list[PoeticSyllable]:
        all_syllables: list[PoeticSyllable] = []
        for phrase in verse.children:
            if isinstance(phrase, String):
                syllables = self.generate_string(phrase)
                all_syllables.extend(syllables)
                continue
            if isinstance(phrase, ManualWord):
                syllables = self.generate_manual_word(phrase)
                all_syllables.extend(syllables)
                continue
            if isinstance(phrase, PiecesTied):
                syllables = self.generate_auto_word(phrase)
                all_syllables.extend(syllables)
                continue
            if isinstance(phrase, PiecesUntied):
                syllables = self.generate_auto_word(phrase)
                all_syllables.extend(syllables)
                continue
            if isinstance(phrase, StressAll):
                syllables = self.generate_all_stressed(phrase)
                all_syllables.extend(syllables)
            if isinstance(phrase, StressNone):
                syllables = self.generate_all_unstressed(phrase)
                all_syllables.extend(syllables)
            if isinstance(phrase, FragmentWord):
                syllables = self.generate_fragment_word(phrase)
                all_syllables.extend(syllables)
        return all_syllables



    def run(self, verse: Verse) -> str:
        poetic_syllables = self.generate_verse(verse)


        num_syllables = len(poetic_syllables)
        last_stress = num_syllables - 1
        for index in reversed(range(num_syllables)):
            if poetic_syllables[index].stress:
                last_stress = index
                break

        output_verse: list[str] = []
        for poetic_syllable in poetic_syllables[0:last_stress + 1]:
            text = poetic_syllable.text(delim='_', stress_prefix='+')
            output_verse.append(text)

        output_rest: list[str] = []
        for poetic_syllable in poetic_syllables[last_stress + 1:]:
            text = poetic_syllable.text(delim='')
            output_rest.append(text)

        if output_rest:
            output_rest_text = f'--{''.join(output_rest)}'
            output_verse.append(output_rest_text)


        output_verse_text = f'|{'|'.join(output_verse)}|'
        return output_verse_text
