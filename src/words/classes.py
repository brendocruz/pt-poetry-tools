from typing import Optional
from src.utils import ReprMixin
from src.syllables.classes import Syllable



class Word(ReprMixin):
    syllables: list[Syllable]

    def __init__(self, syllables: Optional[list[Syllable]] = None):
        self.syllables = [] if syllables is None else syllables


    def __len__(self) -> int:
        return sum([len(syllable) for syllable in self.syllables])


    def text(self) -> str:
        return ''.join([syllable.text() for syllable in self.syllables])
