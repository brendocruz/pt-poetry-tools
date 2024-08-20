from dataclasses import dataclass, field



@dataclass
class Phrase:
    children: tuple['Phrase', ...] = field(default_factory=tuple)

    def __init__(self, *args: 'Phrase') -> None:
        self.children = args



@dataclass(init=False)
class Verse(Phrase):
    pass



@dataclass
class String(Phrase):
    value: str = field(default_factory=str)

    def __init__(self, value: str, *args: Phrase) -> None:
        self.value = value
        super().__init__(*args)


@dataclass
class StringHyphenated(Phrase):
    pass



@dataclass(init=False)
class ManualWord(Phrase):
    pass



@dataclass(init=False)
class FragmentWord(Phrase):
    pass



@dataclass(init=False)
class FragmentStressed(Phrase):
    pass



@dataclass(init=False)
class FragmentString(Phrase):
    pass



@dataclass(init=False)
class FragmentJoin(Phrase):
    pass



@dataclass(init=False)
class FragmentRest(Phrase):
    pass



@dataclass(init=False)
class WordsTied(Phrase):
    pass



@dataclass(init=False)
class WordsUntied(Phrase):
    pass



@dataclass(init=False)
class PiecesTied(Phrase):
    pass



@dataclass(init=False)
class PiecesUntied(Phrase):
    pass



@dataclass(init=False)
class StressAll(Phrase):
    pass



@dataclass(init=False)
class StressNone(Phrase):
    pass
