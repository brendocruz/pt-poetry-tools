import re
from dataclasses import dataclass
from typing import Optional

from src.words.splitter import WordSplitter
from src.stress.finder import StressFinder
from src.verses.patterns import PATTERNS, SUPPORTED_CHARACTERS
# from src.syllables.classes import Syllable, PoeticSyllable
# from src.syllables.flags import DIPHTHONG, STRESS




@dataclass
class VerseSplitter:
    splitter:     WordSplitter
    finder:       StressFinder
    merge_hiatus: Optional[bool] = False
    do_crasis:    Optional[bool] = False


    def run(self, verse: str) -> str:
        # Torna caixa baixa e remove caracteres em branco nas pontas.
        raw_verse = verse.lower().strip()


        # Remove caracteres de pontuação.
        sanitized_verse = ''
        for delim in raw_verse:
            if delim in SUPPORTED_CHARACTERS:
                sanitized_verse += delim
        sanitized_verse = f' {sanitized_verse} '


        # Consume a entrada.
        start_index = 0
        matches: list[tuple[str, str]] = []
        for current_index in range(len(sanitized_verse) + 1):
            for key in PATTERNS.keys():
                pattern = re.compile(PATTERNS[key])
                match = pattern.match(sanitized_verse, start_index, current_index)
                if match:
                    start_match, end_match = match.span()
                    start_index = end_match
                    substring = sanitized_verse[start_match:end_match]
                    matches.append((substring, key))


















        raise NotImplementedError()

#         delims: list[tuple[int, str]] = []
#         raw_syllables: list[Syllable] = []


#         # Quebra o texto de entrada em palavras.
#         start_search = 0
#         pattern      = re.compile(r'\s*(#|-| )\s*')
#         while match := pattern.search(sanitized_verse, start_search):
#             start_match, end_match = match.span()
#             word  = sanitized_verse[start_search:start_match]
#             delim = sanitized_verse[start_match:end_match].strip()

#             word = self.splitter.run(word)
#             self.finder.run(word)
#             raw_syllables.extend(word.syllables)

#             if delim:
#                 delims.append((len(raw_syllables) - 1, delim))
#             start_search = end_match
#         delimdict = dict(delims)


#         # Checa pela última tônica.
#         last_stress: int = -1
#         for index, syllable in reversed(list(enumerate(raw_syllables))):
#             if syllable.has(STRESS):
#                 last_stress = index
#                 break
#         # Se não encontrar nenhuma sílaba tônica, considera a última 
#         # como sendo.
#         if last_stress == -1:
#             last_stress = len(raw_syllables) - 1


#         syllables: list[PoeticSyllable] = []
#         for index in range(last_stress + 2):
#             syllables.append(PoeticSyllable())


#         for index, syllable in enumerate(raw_syllables):
#             if index <= last_stress:
#                 syllables[index].sources.append(syllable)
#             else:
#                 syllables[last_stress + 1].sources.append(syllable)


#         # Une o coda do começo da sílaba anterior à sílaba 
#         # seguinte se ela ele não tem ataque.
#         for index in range(1, last_stress + 2):
#             if not syllables[index].has_onset() and syllables[index - 1].has_coda():
#                 syllables[index].prefix_coda = syllables[index - 1].sources[-1]




#         # Une duas sílbas se a primeira não tiver coda, a segunda não tiver 
#         # ataque, nenhum tiver ditongo e ambas não forem tônicas.
#         merged_syllables: list[PoeticSyllable] = []
#         index = -1
#         while index < last_stress:
#             index += 1
#             if syllables[index].has_coda() or syllables[index + 1].has_onset():
#                 merged_syllables.append(syllables[index])
#                 continue

#             left_syllable  = syllables[index].sources[-1]
#             right_syllable = syllables[index + 1].sources[0]

#             if left_syllable.has(DIPHTHONG, STRESS):
#                 merged_syllables.append(syllables[index])
#                 continue
#             if right_syllable.has(DIPHTHONG, STRESS):
#                 merged_syllables.append(syllables[index])
#                 continue

#             syllables[index].append(syllables[index + 1])
#             merged_syllables.append(syllables[index])
#             index += 1
#         merged_syllables.append(syllables[last_stress + 1])



#         # if self.do_crasis:
#         #     for index in range(last_stress):
#         #         current = syllables[index]
#         #         next    = syllables[index + 1]

#         #         if not output[index]:
#         #             continue

#         #         if not output[index + 1]:
#         #             continue

#         #         if current.has_coda:
#         #             continue

#         #         if next.has_onset:
#         #             continue

#         #         if current.has_diphthong:
#         #             continue

#         #         if next.has_diphthong:
#         #             continue

#         #         if current.nucleus[-1] != next.nucleus[0]:
#         #             continue

#         #         output[index] = f'{output[index]}_{output[index + 1]}'
#         #         output[index + 1] = ''




#         # if self.merge_hiatus:
#         #     for index in range(last_stress):
#         #         current = syllables[index]
#         #         next    = syllables[index + 1]

#         #         if not output[index]:
#         #             continue

#         #         if not output[index + 1]:
#         #             continue

#         #         if current.has_coda:
#         #             continue

#         #         if next.has_onset:
#         #             continue

#         #         if current.has_diphthong:
#         #             continue

#         #         if next.has_diphthong:
#         #             continue

#         #         # XOR lógico.
#         #         if not bool(current.is_stressed) != bool(next.is_stressed):
#         #             continue

#         #         output[index] = f'{output[index]}_{output[index + 1]}'
#         #         output[index + 1] = ''



#         output: list[str] = []
#         for syllable in merged_syllables:
#             output.append(syllable.text('_'))
#         return '|'.join(output)
