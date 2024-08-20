from types import MappingProxyType

SUPPORTED_CHARACTERS    = 'abcdefghijklmnopqrstuvwxyzáéíóúâêôàãõũç\'_-^ '
WORD_CHARACTERS         = 'a-zàáâãéêiíóôõuúç'
WORD_BOUNDARY           = fr'(?= |_|-)'
PATTERN_PLAIN_WORD      = fr' [{WORD_CHARACTERS}]+{WORD_BOUNDARY}'
PATTERN_HYPHENATED_WROD = fr'-[{WORD_CHARACTERS}]+{WORD_BOUNDARY}'
PATTERN_FORCE_SYNALEPHA = fr'_[{WORD_CHARACTERS}]+{WORD_BOUNDARY}'
PATTERN_FORCE_DIPHTHONG = fr' [{WORD_CHARACTERS}^]+{WORD_BOUNDARY}'

PATTERNS = MappingProxyType({
    'plain_word':      PATTERN_PLAIN_WORD,
    'force_synalepha': PATTERN_FORCE_SYNALEPHA,
    'force_diphthong': PATTERN_FORCE_DIPHTHONG,})
