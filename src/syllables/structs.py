ALL_VOWELS           = ('a', 'e', 'i', 'o', 'u', 'á', 'é', 'í', 'ó', 
                        'ú', 'â', 'ê', 'ô', 'à', 'ã', 'õ', 'ũ')
NO_ACCENT_VOWELS     = ('a', 'e', 'i', 'o', 'u')
CONSONANTS           = ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'l', 'm', 
                        'n', 'p', 'q', 'r', 's', 't', 'v', 'x', 'z', 'ç')
DIPHTHONG_POSSIBLY   = ('ai', 'ei', 'oi', 'ui', 'au', 'eu', 'iu', 'ou')
DIPHTHONG_ALWAYS     = ('ãe', 'ão', 'õe', 'ãi', 'âi', 'ũa',
                        'ái', 'áu', 'éi', 'êi', 'éu', 'êu', 'ói')
HIATUS_ALWAYS        = ('aa', 'ee', 'ii', 'oo', 'uu')
HIATUS_ALWAYS_END    = ('a', 'á', 'â', 'ã', 'e', 'é', 'ê', 'o', 'ó',
                        'ô', 'õ', 'í', 'ú')
HIATUS_ACCENT_STOP   = ('l', 'm', 'n', 'r', 'z') # nh.
ONSET_CLUSTER        = ('cc', 'cç', 'ct', 'pt', 'pç', 'pc', 'bs', 'bv', 'ps', 
                        'dm', 'dv', 'tm', 'gn', 'bm', 'cn', 'bj', 'mn')
ONSET_CLUSTER_END    = ('l', 'r')
CODA                 = ('h', 'l', 'm', 'n', 'r', 's', 'x', 'z')
TRIGRAPH             = ('tch')
DIGRAPHS_ALWAYS      = ('lh', 'nh', 'rr', 'ss', 'sç', 'ch', 'qu', 'xs', 'gd')
DIGRAPHS_SOMETIMES_1 = ('xc', 'sc')
DIGRAPHS_SOMETIMES_2 = ('gu')
DIGRAPHS_PREVENT     = ('a', 'á', 'â', 'ã', 'o', 'ó', 'ô', 'õ', 'u', 'ú')
CODA_MIDDLE          = ('l', 'm', 'n', 'r', 's', 'x', 'z')
CODA_END             = ('h', 'l', 'm', 'n', 'r', 's', 'x', 'z')
CODA_CLUSTER_MIDDLE  = ('ns')
CODA_CLUSTER_END     = ('ns', 'ps')
SPECIAL_SYMBOLS      = ("'", '’')
PREFIXES             = ('-')

ALL_ONSET_DIGRAPHS   = ('lh', 'nh', 'rr', 'ss', 'sç', 'ch', 
                        'qu', 'xs', 'gd', 'xc', 'sc', 'gu')
