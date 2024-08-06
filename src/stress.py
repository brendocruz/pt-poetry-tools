from src.words import Word



STRESSABLE_VOWELS   = ('á', 'é', 'í', 'ó', 'ú', 'â', 'ê', 'ô')
PAROXYTONE_ENDS     = ('ão', 'ãos')
OXYTONE_ENDS        = ('a', 'as', 'e', 'es', 'o', 'os', 'em', 'ens')



class StressFinder():
    def __init__(self):
        pass

    def run(self, word: Word) -> int:
        wordlen = len(word.syllables)

        count = 0
        # Checando por acentos que indiquem a sílaba tônica da palavra.
        for index in range(wordlen - 1, -1, -1):
            # Sílabas "sem núcleo" são ignoradas, porque eles não inteferen
            # na tonicidade de uma palavra.
            if not word.syllables[index].has_nucleus:
                continue

            # Checa apenas o primeiro índice do núcleo, porque, mesmo nos 
            # casos de ditongo, vai ser a primeira letra que vai ter o acento.
            if word.syllables[index].nucleus[0] in STRESSABLE_VOWELS:
                return index 
            count += 1

            # A checagem é feita apenas nas três últimas sílabas, porque são 
            # as únicas que podem ser tônicas na língua portuguesa.
            if count == 3:
                break


        wordstr = word.get()


        # Checando por oxítonas. Essa checagem só é feito, porque a terminação
        # "ão" que torna as palavras oxítonas se confudem com a terminação "o"
        # que torna as palavras paroxítonas (quando acentuadas ao menos).
        if wordstr.endswith(PAROXYTONE_ENDS):
            if word.syllables[wordlen - 1].has_nucleus:
                return wordlen - 1
            return wordlen - 2


        # Checando por paroxítonas.
        if wordstr.endswith(OXYTONE_ENDS):
            if word.syllables[wordlen - 2].has_nucleus:
                return wordlen - 2
            return wordlen - 3


        # Todas as palavras que não passarem nos testes acima são consideras
        # paroxítonas. Os testes acima devem pegar 100% das palavras que não
        # são paroxítonas e que seguem os padrões de acentuação e grafia da
        # língua portuguesa. Além disso, paroxítonas é o padrão da língua, se
        # por acaso houver alguma palavra não segue o padrão, é bem provável
        # que ela seja paroxítonas.


        if word.syllables[wordlen - 1].has_nucleus:
            return wordlen - 1
        return wordlen - 2
