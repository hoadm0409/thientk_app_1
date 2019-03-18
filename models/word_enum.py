from enum import Enum


class WordKindEnum(Enum):
    NEG = 1
    POS = 2

    def __str__(self):
        return self.name


class WordTypeEnum(Enum):
    VERB = 1
    ADJ = 2

    def __str__(self):
        return self.name
