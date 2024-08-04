from dataclasses import dataclass
from typing import Optional

from src.utils import ReprMixin
from src.syllables import Syllable, SyllableSplitter



class Word(ReprMixin):
    syllables: list[Syllable]

    def __init__(self, syllables: Optional[list[Syllable]] = None):
        self.syllables = [] if syllables is None else syllables

    def __len__(self) -> int:
        return sum([len(syllable) for syllable in self.syllables])

    def get(self) -> str:
        return ''.join([syllable.get() for syllable in self.syllables])




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
