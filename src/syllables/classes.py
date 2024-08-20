from dataclasses import dataclass, field
from typing import Optional
from src.syllables.flags import CODA, ONSET, STRESS



@dataclass
class Syllable:
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


    def merge(self, other: 'Syllable') -> Optional['Syllable']:
        if other.prefix != '':
            return None

        if self.coda != '':
            return None

        if other.onset != '':
            return None

        prefix  = self.prefix
        onset   = self.onset
        nucleus = self.nucleus + other.nucleus
        coda    = other.coda

        syllable = Syllable(prefix=prefix, onset=onset, nucleus=nucleus, coda=coda)
        syllable.set_props(self.props, other.props)
        return syllable


    def text(self) -> str:
        return f'{self.prefix}{self.onset}{self.nucleus}{self.coda}'


    def parts(self) -> list[str]:
        return [self.prefix, self.onset, self.nucleus, self.coda]

    
    def __len__(self) -> int:
        return len(self.text())




@dataclass
class PoeticSyllable:
    prefix_coda:  Optional[Syllable] = None
    sources:          list[Syllable] = field(default_factory=list)
    stress:                     bool = False



    def __post_init__(self):
        for syllable in self.sources:
            if syllable.has(STRESS):
                self.stress = True



    def is_empty(self) -> bool:
        if self.prefix_coda:
            return False
        if self.sources:
            return False
        return True



    def text(self, delim: str, stress_prefix: str = '') -> str:
        source_text: list[str] = []
        if self.prefix_coda:
            source_text.append(self.prefix_coda.coda)

        for syllable in self.sources:
            source_text.append(syllable.text())

        output_text = delim.join(source_text)
        if self.stress:
            output_text = f'{stress_prefix}{output_text}'
        
        return output_text


    
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



    def add_prefix(self, syllable):
        self.prefix_coda = syllable


    
    def append(self, syllable: Syllable):
        self.sources.append(syllable)
        if syllable.has(STRESS):
            self.stress = True



    def extend(self, other: 'PoeticSyllable'):
        self.sources.extend(other.sources)
        for syllable in other.sources:
            if syllable.has(STRESS):
                self.stress = True
