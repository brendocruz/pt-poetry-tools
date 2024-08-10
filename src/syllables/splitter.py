from dataclasses import dataclass
from typing import Optional

from src.syllables.classes import Syllable
from src.syllables.structs import *
import src.syllables.flags as f
from src.utils import ReprMixin




@dataclass
class SyllableSplitterBase(ReprMixin):
    split_onset_cluster: bool = False




@dataclass
class SyllableSplitter(SyllableSplitterBase):
    def run(self, word: str, index: int, syllable: Optional[Syllable] = None) -> tuple[Syllable, int]:
        if not syllable:
            syllable = Syllable()
        return SyllableSplitterStart(**vars(self)).run(word, index, syllable)




@dataclass
class SyllableSplitterStart(SyllableSplitterBase):
    def run(self, word: str, index: int, syllable: Syllable) -> tuple[Syllable, int]:
        return SyllableSplitterOnset(**vars(self)).run(word, index, syllable)





@dataclass
class SyllableSplitterOnset(SyllableSplitterBase):
    def run(self, word: str, index: int, syllable: Syllable) -> tuple[Syllable, int]:
        wordlen = len(word)


        # Este método vai continuar sendo chamado recursivamente até ser 
        # capaz de processar toda uma sequência contígua de caracteres
        # composta de consoantes e apóstrofos, sendo ela terminada por vogal.


        # Checando por apóstrofos. 
        if word[index] in SPECIAL_SYMBOLS:
            syllable.onset += word[index]
            syllable.set_props(f.ONSET)
            return SyllableSplitterOnset(**vars(self)).run(word, index + 1, syllable)


        # Checando por vogais.
        if word[index] in ALL_VOWELS:
            return SyllableSplitterNucleus(**vars(self)).run(word, index, syllable)


        # Checando por trígrafos.
        if index + 3 < wordlen:
            if word[index:index + 3] in TRIGRAPH:
                syllable.onset += word[index:index + 3]
                syllable.set_props(f.ONSET, f.ONSET_DIGRAPH)
                return SyllableSplitterOnset(**vars(self)).run(word, index + 3, syllable)


        # Checando por sequências de duas consoantes,
        # sejam elas dígrafos ou encontros consonantais.
        if index + 2 < wordlen:
            # Sequências que são sempre dígrafo.
            if word[index:index + 2] in DIGRAPHS_ALWAYS:
                syllable.onset += word[index:index + 2]
                syllable.set_props(f.ONSET, f.ONSET_DIGRAPH)
                return SyllableSplitterOnset(**vars(self)).run(word, index + 2, syllable)

            # Sequências que são dígrafo às vezes. Não influencia no ataque,
            # mas estar separado, porque influencia na separação da coda.
            if word[index:index + 2] in DIGRAPHS_SOMETIMES_1:
                syllable.onset += word[index:index + 2]
                syllable.set_props(f.ONSET, f.ONSET_DIGRAPH)
                return SyllableSplitterOnset(**vars(self)).run(word, index + 2, syllable)

            # Sequências que são dígrafo às vezes. Sendo unicamente o caso 
            # de `gu`, que só é dígrafo quando seguido de uma vogal.
            if word[index:index + 2] in DIGRAPHS_SOMETIMES_2:
                if word[index + 2] in CONSONANTS:
                    syllable.onset += word[index]
                    syllable.set_props(f.ONSET)
                    return SyllableSplitterOnset(**vars(self)).run(word, index + 1, syllable)
                syllable.onset += word[index:index + 2]
                syllable.set_props(f.ONSET, f.ONSET_DIGRAPH)
                return SyllableSplitterOnset(**vars(self)).run(word, index + 2, syllable)

            # Checando por encontros consonantais terminados por `r` e `l`.
            if word[index + 1] in ONSET_CLUSTER_END:
                syllable.onset += word[index:index + 2]
                syllable.set_props(f.ONSET, f.ONSET_CLUSTER)
                return SyllableSplitterOnset(**vars(self)).run(word, index + 2, syllable)

            # Checando por encontros consonantais.
            if word[index:index + 2] in ONSET_CLUSTER:
                if not self.split_onset_cluster:
                    syllable.onset += word[index:index + 2]
                    syllable.set_props(f.ONSET, f.ONSET_CLUSTER)
                    return SyllableSplitterOnset(**vars(self)).run(word, index + 2, syllable)
                else:
                    syllable.onset += word[index]
                    syllable.set_props(f.ONSET)
                    return SyllableSplitterEnd(**vars(self)).run(word, index + 1, syllable)


        # Se chegar até aqui, deve ser consoante.
        syllable.onset += word[index]
        syllable.set_props(f.ONSET)
        return SyllableSplitterOnset(**vars(self)).run(word, index + 1, syllable)




@dataclass
class SyllableSplitterNucleus(SyllableSplitterBase):

    def is_diphthong(self, __word__: str, __index__: int) -> bool:
        return True


    def run(self, word: str, index: int, syllable: Syllable) -> tuple[Syllable, int]:
        wordlen  = len(word)

        # Checando por vogais no fim de palavra.
        if index + 1 == wordlen:
            syllable.nucleus = word[index]
            syllable.set_props(f.NUCLEUS)
            return SyllableSplitterCoda(**vars(self)).run(word, index + 1, syllable)


        # Checando por vogais antes de consoante.
        if word[index + 1] in CONSONANTS:
            syllable.nucleus = word[index]
            syllable.set_props(f.NUCLEUS)
            return SyllableSplitterCoda(**vars(self)).run(word, index + 1, syllable)


        # NOTE: Talvez seja redundante?
        if index + 2 <= wordlen:
            # Checando por encontro vocálicos que são sempre ditongo.
            if word[index:index + 2] in DIPHTHONG_ALWAYS:
                syllable.nucleus = word[index:index + 2]
                syllable.set_props(f.NUCLEUS, f.DIPHTHONG)
                return SyllableSplitterCoda(**vars(self)).run(word, index + 2, syllable)

            # Checando por hiatos formados pelo encontro na mesma vogal.
            if word[index:index + 2] in HIATUS_ALWAYS:
                syllable.nucleus = word[index]
                syllable.set_props(f.NUCLEUS)
                return SyllableSplitterCoda(**vars(self)).run(word, index + 1, syllable)

            # Checando por encontros vocálicos que sempre são hiato.
            if word[index + 1] in HIATUS_ALWAYS_END:
                syllable.nucleus = word[index]
                syllable.set_props(f.NUCLEUS)
                return SyllableSplitterCoda(**vars(self)).run(word, index + 1, syllable)
            
            # TODO: Conferir se isso está correto.
            if index + 3 == wordlen:
                if word[index + 2] in HIATUS_ACCENT_STOP:
                    syllable.nucleus = word[index]
                    syllable.set_props(f.NUCLEUS)
                    return SyllableSplitterCoda(**vars(self)).run(word, index + 1, syllable)

            # TODO: Conferir se isso está correto.
            # Check for hiatus on `i` and `u` with no accent
            # in the middle of the word.
            if index + 3 < wordlen:
                if word[index + 2] in HIATUS_ACCENT_STOP:
                    if word[index + 3] in CONSONANTS:
                        if word[index + 2:index + 4] != 'lh':
                            syllable.nucleus = word[index]
                            syllable.set_props(f.NUCLEUS)
                            return SyllableSplitterCoda(**vars(self)).run(word, index + 1, syllable)

        if word[index:index + 2] in DIPHTHONG_POSSIBLY:
            if self.is_diphthong(word, index):
                syllable.nucleus = word[index:index + 2]
                syllable.set_props(f.NUCLEUS)
                return SyllableSplitterCoda(**vars(self)).run(word, index + 2, syllable)
            # else:
            #     syllable.nucleus = word[index]
            #     syllable.set_props(f.NUCLEUS)
            #     return SyllableSplitterCoda(**vars(self)).run(word, index + 1, syllable)




@dataclass
class SyllableSplitterCoda(SyllableSplitterBase):
    def run(self, word: str, index: int, syllable: Syllable) -> tuple[Syllable, int]:
        wordlen  = len(word)

        # Checando por índice depois do final da palavra, ou seja, não tem coda.
        if index == wordlen:
            return SyllableSplitterEnd(**vars(self)).run(word, index, syllable)

        # Checando por coda simples no final da palavra.
        if index + 1 == wordlen:
            if word[index] in CODA_END:
                syllable.coda = word[index]
                syllable.set_props(f.CODA)
                return SyllableSplitterEnd(**vars(self)).run(word, index + 1, syllable)

        # Checando por encontro consonantal no final da palavra.
        if index + 2 == wordlen:
            if word[index:index + 2] in CODA_CLUSTER_END:
                syllable.coda = word[index:index + 2]
                syllable.set_props(f.CODA, f.CODA_CLUSTER)
                return SyllableSplitterEnd(**vars(self)).run(word, index + 2, syllable)

        # Checando por encontro consonantal no meio da palavra.
        if index + 3 < wordlen:
            if word[index:index + 2] in CODA_CLUSTER_MIDDLE:
                if word[index + 2] in CONSONANTS:
                    syllable.coda = word[index:index + 2]
                    syllable.set_props(f.CODA, f.CODA_CLUSTER)
                    return SyllableSplitterEnd(**vars(self)).run(word, index + 2, syllable)

        if word[index:index + 2] in DIGRAPHS_ALWAYS:
            return SyllableSplitterEnd(**vars(self)).run(word, index, syllable)


        # Checar pelas sequências `xc` e `sc` que vezes são dígrafos, vezes não.
        # São dígrafos quando seguidos de `e`, `i` e suas variantes acentuadas.
        if word[index:index + 2] in DIGRAPHS_SOMETIMES_1:
            if word[index + 2] in ALL_VOWELS:
                if word[index + 2] in DIGRAPHS_PREVENT:
                    syllable.coda = word[index]
                    syllable.set_props(f.CODA)
                    return SyllableSplitterEnd(**vars(self)).run(word, index + 1, syllable)
                return SyllableSplitterEnd(**vars(self)).run(word, index, syllable)
            syllable.coda = word[index]
            syllable.set_props(f.CODA)
            return SyllableSplitterEnd(**vars(self)).run(word, index + 1, syllable)


        if word[index] in CODA_MIDDLE:
            if word[index + 1] in CONSONANTS:
                syllable.coda = word[index]
                syllable.set_props(f.CODA)
                return SyllableSplitterEnd(**vars(self)).run(word, index + 1, syllable)

        return SyllableSplitterEnd(**vars(self)).run(word, index, syllable)




@dataclass
class SyllableSplitterEnd(SyllableSplitterBase):
    def run(self, word: str, index: int, syllable: Syllable) -> tuple[Syllable, int]:
        if word: pass
        return (syllable, index)
