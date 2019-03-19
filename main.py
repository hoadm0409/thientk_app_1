import os
from models import VNDict, WordTypeEnum
from utilities import load_input_word_list, load_vn_dict
from utilities import find_nearest_word, write_csv
from utilities import Setting
from utilities import greedy

APP_DIR = os.path.dirname(__file__)


if __name__ == '__main__':
    # load word_list && vn_dict
    # input_data_file = APP_DIR + '/data/input/debug.txt'
    input_data_file = APP_DIR + '/data/input/word_list.txt'
    input_word_list = load_input_word_list(input_data_file)
    load_vn_dict()
    vn_dict = VNDict.get_instance()

    # analyze
    results = {
        WordTypeEnum.VERB: [],
        WordTypeEnum.ADJ: []
    }

    for input_word in input_word_list:
        words_were_found = vn_dict.look_up(input_word.txt, w_kind=input_word.kind)
        if not words_were_found:
            continue

        nearest_word = find_nearest_word(input_word, words_were_found)
        results[nearest_word.type].append(nearest_word)

    if Setting.GREEDY:
        additional_verbs, additional_adjectives = greedy(results, Setting.GREEDY_ALGORITHMS)
        results[WordTypeEnum.VERB] = results[WordTypeEnum.VERB] + additional_verbs
        results[WordTypeEnum.ADJ] = results[WordTypeEnum.ADJ] + additional_adjectives

    write_csv(APP_DIR + '/data/output/{}.txt'.format(WordTypeEnum.VERB.name), results[WordTypeEnum.VERB])
    write_csv(APP_DIR + '/data/output/{}.txt'.format(WordTypeEnum.ADJ.name), results[WordTypeEnum.ADJ])

