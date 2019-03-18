import os
from models import Word, WordKindEnum
from utilities import Setting


def load_input_word_list(file_path):
    """
    Load word list from text file

    :param file_path: path to data file
    :return: List of Words if file_path is valid. False otherwise
    """
    if not os.path.isfile(file_path):
        return False

    word_list = list()

    with open(file_path, 'r') as fp:
        while True:
            line = fp.readline()
            if not line:
                break

            data = line.split(' ')
            text = data[0].lower().strip(Setting.NONWORD_CHARACTERS)

            if not text:
                continue

            score = float(data[1])

            if score < 0:
                kind = WordKindEnum.NEG
            else:
                kind = WordKindEnum.POS

            word = Word(text, score, kind)
            word_list.append(word)

    return word_list
