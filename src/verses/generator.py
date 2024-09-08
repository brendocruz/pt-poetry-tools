from typing import cast

from src.verses.nodes import *
from src.words.classes import Word
from src.syllables.classes import PoeticSyllable, Syllable
from src.words.splitter import WordSplitter
from src.stress.finder import StressFinder


class VerseGenerator:
    splitter: WordSplitter
    finder: StressFinder

    def __init__(self, splitter: WordSplitter, finder: StressFinder):
        self.splitter = splitter
        self.finder = finder


    def generate_tied_words(self, words: WordsTied) -> list[PoeticSyllable]:
        all_syllables: list[list[PoeticSyllable]] = []
        for child in words.children:
            syllables = self.generate_phrase(child)
            all_syllables.append(syllables)

        left_word  = all_syllables[0]
        right_word = all_syllables[1]
        left_edge  = left_word.pop(-1)
        right_edge = right_word.pop(0)

        joined_words: list[PoeticSyllable] = []
        if not left_edge.has_coda() and not right_edge.has_onset():
            left_edge.extend(right_edge)
            joined_words.extend(left_word)
            joined_words.append(left_edge)
            joined_words.extend(right_word)
            return joined_words

        joined_words.extend(left_word)
        joined_words.append(left_edge)
        joined_words.append(right_edge)
        joined_words.extend(right_word)
        return joined_words



    def generate_untied_words(self, words: WordsUntied) -> list[PoeticSyllable]:
        all_syllables: list[list[PoeticSyllable]] = []
        for child in words.children:
            syllables = self.generate_phrase(child)
            all_syllables.append(syllables)

        left_word  = all_syllables[0]
        right_word = all_syllables[1]

        left_word[-1].mergeable = False
        right_word[0].mergeable = False

        joined_words: list[PoeticSyllable] = []
        joined_words.extend(left_word)
        joined_words.extend(right_word)
        return joined_words



    def generate_full_word(self, full_word: Phrase) -> list[PoeticSyllable]:
        poetic_syllables: list[PoeticSyllable] = []
        if isinstance(full_word, WordsTied):
            poetic_syllables = self.generate_tied_words(full_word)
        elif isinstance(full_word, WordsUntied):
            poetic_syllables = self.generate_untied_words(full_word)
        return poetic_syllables



    def generate_untied_pieces(self, pieces: PiecesUntied) -> list[PoeticSyllable]:
        all_syllables: list[list[PoeticSyllable]] = []
        for child in pieces.children:
            if isinstance(child, String):
                syllables = self.split_string_2(child)
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

        left_piece[-1].mergeable = False
        right_piece[0].mergeable = False

        joined_pieces: list[PoeticSyllable] = []
        joined_pieces.extend(left_piece)
        joined_pieces.extend(right_piece)
        return joined_pieces



    def generate_tied_pieces(self, pieces: PiecesTied) -> list[PoeticSyllable]:
        all_syllables: list[list[PoeticSyllable]] = []
        for child in pieces.children:
            if isinstance(child, String):
                syllables = self.split_string_2(child)
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

        joined_pieces: list[PoeticSyllable] = []
        if not left_edge.has_coda() and not right_edge.has_onset():
            left_edge.extend(right_edge)
            joined_pieces.extend(left_piece)
            joined_pieces.append(left_edge)
            joined_pieces.extend(right_piece)
            return joined_pieces

        joined_pieces.extend(left_piece)
        joined_pieces.append(left_edge)
        joined_pieces.append(right_edge)
        joined_pieces.extend(right_piece)
        return joined_pieces



    def generate_auto_word(self, auto_word: Phrase) -> list[PoeticSyllable]:
        poetic_syllables: list[PoeticSyllable] = []

        if isinstance(auto_word, PiecesTied):
            poetic_syllables = self.generate_tied_pieces(auto_word)
        elif isinstance(auto_word, PiecesUntied):
            poetic_syllables = self.generate_untied_pieces(auto_word)


        unpacked_syllables: list[Syllable] = []
        for poetic_syllable in poetic_syllables:
            unpacked_syllables.extend(poetic_syllable.sources)

        merged_word = Word(unpacked_syllables)
        regular_word = self.splitter.run(merged_word.text())
        stress_index = self.finder.run(regular_word)


        # Checa se a palavra é átona.
        # if stress_index == -1:
        #     return merged_word.syllables

        start, end = regular_word.span_text(stress_index)
        indices    = merged_word.span_syllable(start, end)
        choose     = indices[0]
        merged_word.syllables[choose].stress = True


        target_syllable = merged_word.syllables[choose]
        for poetic_syllable in poetic_syllables:
            if target_syllable in poetic_syllable.sources:
                poetic_syllable.stress = True
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


    def split_string_2(self, string: String) -> list[PoeticSyllable]:
        word = self.splitter.run(string.value)
        poetic_syllables: list[PoeticSyllable] = []
        for syllable in word.syllables:
            poetic_syllable = PoeticSyllable(sources=[syllable])
            poetic_syllables.append(poetic_syllable)
        return poetic_syllables


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
            syllable.stress = True

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



    def generate_phrase(self, phrase: Phrase) -> list[PoeticSyllable]:
        if isinstance(phrase, String):
            syllables = self.generate_string(phrase)
            return syllables
        if isinstance(phrase, ManualWord):
            syllables = self.generate_manual_word(phrase)
            return syllables
        if isinstance(phrase, PiecesTied):
            syllables = self.generate_auto_word(phrase)
            return syllables
        if isinstance(phrase, PiecesUntied):
            syllables = self.generate_auto_word(phrase)
            return syllables
        if isinstance(phrase, StressAll):
            syllables = self.generate_all_stressed(phrase)
            return syllables
        if isinstance(phrase, StressNone):
            syllables = self.generate_all_unstressed(phrase)
            return syllables
        if isinstance(phrase, FragmentWord):
            syllables = self.generate_fragment_word(phrase)
            return syllables
        if isinstance(phrase, WordsTied):
            syllables = self.generate_full_word(phrase)
            return syllables
        if isinstance(phrase, WordsUntied):
            syllables = self.generate_full_word(phrase)
            return syllables
        return []



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
                continue
            if isinstance(phrase, StressNone):
                syllables = self.generate_all_unstressed(phrase)
                all_syllables.extend(syllables)
                continue
            if isinstance(phrase, FragmentWord):
                syllables = self.generate_fragment_word(phrase)
                all_syllables.extend(syllables)
            if isinstance(phrase, WordsTied):
                syllables = self.generate_full_word(phrase)
                all_syllables.extend(syllables)
                continue
            if isinstance(phrase, WordsUntied):
                syllables = self.generate_full_word(phrase)
                all_syllables.extend(syllables)
                continue
        return all_syllables


    
    def merge_syllables_hiatus(self, syllables: list[PoeticSyllable], 
                               start: int, end: int) -> list[PoeticSyllable]:
        # Une duas sílbas se a primeira não tiver coda, a segunda não tiver 
        # ataque, nenhum tiver ditongo e ambas não forem tônicas.
        index = start
        merged_syllables: list[PoeticSyllable] = []

        # for syllable in syllables[:start]:
        #     merged_syllables.append(syllable)

        while index < end - 1:
            left_syllable = syllables[index]
            right_syllable = syllables[index + 1]

            if left_syllable.stress and right_syllable.stress:
                merged_syllables.append(left_syllable)
                index += 1
                continue

            if not left_syllable.mergeable:
                merged_syllables.append(left_syllable)
                index += 1
                continue


            if not right_syllable.mergeable:
                merged_syllables.append(left_syllable)
                index += 1
                continue

            if left_syllable.has_coda():
                merged_syllables.append(left_syllable)
                index += 1
                continue

            if right_syllable.has_onset():
                merged_syllables.append(left_syllable)
                index += 1
                continue

            if len(left_syllable.sources) > 1:
                merged_syllables.append(left_syllable)
                index += 1
                continue

            # if len(right_syllable.sources) > 1:
            #     merged_syllables.append(left_syllable)
            #     index += 1
            #     continue

            if left_syllable.sources[0].has_diphthong():
                merged_syllables.append(left_syllable)
                index += 1
                continue

            if right_syllable.sources[0].has_diphthong():
                merged_syllables.append(left_syllable)
                index += 1
                continue

            left_syllable.extend(right_syllable)
            merged_syllables.append(left_syllable)
            index += 2

        # if end < 1:
        #     end = 1

        for syllable in syllables[end - 1:]:
            merged_syllables.append(syllable)

        return merged_syllables



    def merge_syllables_coda_prefix(self, syllables: list[PoeticSyllable], 
                                    start: int, end: int) -> list[PoeticSyllable]:
        index = start
        while index < end - 1:
            left_syllable = syllables[index]
            right_syllable = syllables[index + 1]

            if not left_syllable.has_coda():
                index += 1
                continue
            if right_syllable.has_onset():
                index += 1
                continue

            right_syllable.add_prefix(left_syllable)
            index += 1
        return syllables



    def get_last_stress(self, syllables: list[PoeticSyllable]) -> int:
        num_syllables = len(syllables)
        last_stress = num_syllables - 1
        for index in reversed(range(num_syllables)):
            if syllables[index].stress:
                last_stress = index
                break
        return last_stress



    def generate_output(self, poetic_syllables: list[PoeticSyllable]) -> str:
        last_stress = self.get_last_stress(poetic_syllables)

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



    def run(self, verse: Verse) -> str:
        poetic_syllables = self.generate_verse(verse)

        last_stress = self.get_last_stress(poetic_syllables)
        merged_syllables = self.merge_syllables_hiatus(poetic_syllables, 0, last_stress + 1)

        last_stress = self.get_last_stress(merged_syllables)
        merged_syllables = self.merge_syllables_coda_prefix(merged_syllables, 0, last_stress + 1)
        output_verse_text = self.generate_output(merged_syllables)
        return output_verse_text
