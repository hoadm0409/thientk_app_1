from models import Word, WordKindEnum


def find_nearest_word(center, word_list):
    nearest_word = word_list[0]

    if center.kind == WordKindEnum.POS:
        nearest_score = abs(abs(nearest_word.score) - abs(center.score))
        for word in word_list:
            score = abs(abs(word.score) - abs(center.score))
            if score < nearest_score:
                nearest_score = score
                nearest_word = word

        return Word(nearest_word.txt, nearest_score, nearest_word.kind, nearest_word.type)
    else:
        nearest_score = abs(abs(nearest_word.score) - abs(center.score))
        for word in word_list:
            score = abs(abs(word.score) - abs(center.score))
            if score < nearest_score:
                nearest_score = score
                nearest_word = word

        return Word(nearest_word.txt, nearest_score * (-1), nearest_word.kind, nearest_word.type)

