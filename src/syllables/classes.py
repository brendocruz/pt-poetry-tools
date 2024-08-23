from dataclasses import dataclass, field
from typing import Optional
from src.syllables.structs import ALL_ONSET_DIGRAPHS



@dataclass
class Syllable:
    prefix:   str = ''
    onset:    str = ''
    nucleus:  str = ''
    coda:     str = ''
    stress:  bool = False


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
        if self.has_stress() or other.has_stress():
            syllable.stress = True
        return syllable


    def text(self) -> str:
        return f'{self.prefix}{self.onset}{self.nucleus}{self.coda}'


    def parts(self) -> list[str]:
        return [self.prefix, self.onset, self.nucleus, self.coda]

    
    def __len__(self) -> int:
        return len(self.text())

    def has_onset(self) -> bool:
        return self.onset != ''

    def has_coda(self) -> bool:
        return self.coda != ''

    def has_nucleus(self) -> bool:
        return self.nucleus != ''

    def has_diphthong(self) -> bool:
        return len(self.nucleus) > 1

    def has_onset_digraph(self) -> bool:
        return self.onset in ALL_ONSET_DIGRAPHS

    def has_onset_cluster(self) -> bool:
        if len(self.onset) <= 1:
            return False
        if self.onset in ALL_ONSET_DIGRAPHS:
            return False
        return True

    def has_coda_cluster(self) -> bool:
        return len(self.coda) > 1

    def has_stress(self) -> bool:
        return self.stress







@dataclass
class PoeticSyllable:
    prefix:     Optional[str] = None
    sources:   list[Syllable] = field(default_factory=list)
    stress:              bool = False
    mergeable:           bool = True



    def __post_init__(self):
        for syllable in self.sources:
            if syllable.has_stress():
                self.stress = True



    def is_empty(self) -> bool:
        if self.prefix:
            return False
        if self.sources:
            return False
        return True



    def text(self, delim: str, stress_prefix: str = '') -> str:
        source_text: list[str] = []
        if self.prefix:
            source_text.append(self.prefix)

        for syllable in self.sources:
            source_text.append(syllable.text())

        output_text = delim.join(source_text)
        if self.stress:
            output_text = f'{stress_prefix}{output_text}'
        
        return output_text


    
    def has_onset(self) -> bool:
        if self.prefix:
            return True
        if not self.sources:
            return False
        return self.sources[0].has_onset()



    def has_coda(self) -> bool:
        if not self.sources:
            return False
        return self.sources[-1].has_coda()



    def add_prefix(self, other: 'PoeticSyllable') -> None:
        target = other.sources[-1]
        codalen = len(target.coda)

        if codalen == 1:
            self.prefix = target.coda
            target.coda = ''
            return
        if codalen > 1:
            coda = target.coda
            new_onset = coda[-1]
            new_coda  = coda[:-1]
            self.prefix = new_onset
            target.coda = new_coda
            return


    
    def append(self, syllable: Syllable):
        self.sources.append(syllable)
        if syllable.has_stress():
            self.stress = True



    def extend(self, other: 'PoeticSyllable'):
        self.sources.extend(other.sources)
        for syllable in other.sources:
            if syllable.has_stress():
                self.stress = True
