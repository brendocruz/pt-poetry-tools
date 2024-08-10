from dataclasses import dataclass
from src.syllables.splitter import SyllableSplitter
from src.words.classes import Word



@dataclass
class WordSplitter:
    split_onset_cluster: bool = False

    def run(self, word: str) -> Word:
        index = 0
        wordlen = len(word)
        syllables = []

        while index < wordlen:
            splitter = SyllableSplitter(**vars(self))
            syllable, index = splitter.run(word, index)
            syllables.append(syllable)
        return Word(syllables)
