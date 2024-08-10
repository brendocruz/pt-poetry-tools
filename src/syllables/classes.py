from dataclasses import dataclass, field
from typing import Optional
from src.syllables.flags import CODA, ONSET
from src.utils import ReprMixin



@dataclass
class Syllable(ReprMixin):
    prefix:  str = field(default_factory=str)
    onset:   str = field(default_factory=str)
    nucleus: str = field(default_factory=str)
    coda:    str = field(default_factory=str)
    props:   int = field(default_factory=int)


    def has(self, *props: int) -> bool:
        for prop in props:
            if not self.props & prop == prop:
                return False
        return True


    def set_props(self, *props: int) -> None:
        for prop in props:
            self.props |= prop


    def text(self) -> str:
        return f'{self.prefix}{self.onset}{self.nucleus}{self.coda}'


    def parts(self) -> list[str]:
        return [self.prefix, self.onset, self.nucleus, self.coda]

    
    def __len__(self) -> int:
        return len(self.text())


    def __repr__(self) -> str:
        return super().__repr__()




@dataclass
class PoeticSyllable:
    prefix_coda:  Optional[Syllable] = None
    sources:          list[Syllable] = field(default_factory=list)


    def is_empty(self) -> bool:
        if self.prefix_coda:
            return False
        if self.sources:
            return False
        return True



    def text(self, delim: str) -> str:
        text = ''
        if self.prefix_coda:
            text += self.prefix_coda.coda
        for syllable in self.sources:
            text += f'{delim}{syllable.text()}'
        if not self.prefix_coda:
            return text[1:]
        return text


    
    def has_onset(self) -> bool:
        if self.prefix_coda:
            return True
        if not self.sources:
            return False
        return self.sources[0].has(ONSET)



    def has_coda(self) -> bool:
        if not self.sources:
            return False
        return self.sources[-1].has(CODA)



    def append(self, other: 'PoeticSyllable'):
        self.sources.extend(other.sources)
