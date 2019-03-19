from utilities import get_db_connect_string
from utilities import Setting
from models import Word, WordTypeEnum, WordKindEnum
from sqlalchemy import create_engine
from sqlalchemy.sql import text

"""
    data: dữ liệu đã được xử lý trước đó. là 1 dict có cấu trúc:
    {
        VERB: [],
        ADJ: []
    }
    ,
    tìm các từ trong từ điển, chưa tồn tại trong data.
"""
def filter_word_list(data):
    """
        trả về tuples (LIST_VERB, LIST_ADJ)
    """
    engine = create_engine(get_db_connect_string())
    conn = engine.connect()

    # Verbs
    verbs_used = list()
    for verb in data[WordTypeEnum.VERB]:
        verbs_used.append(verb.txt)

    verb_query_string_statement = text("SELECT PosScore, NegScore, SynsetTerm FROM verb")
    verbs = conn.execute(verb_query_string_statement).fetchall()

    verbs_unused = dict()
    for verb in verbs:
        verb_text = verb.SynsetTerm.lower().strip(Setting.NONWORD_CHARACTERS)
        if verb_text not in verbs_used:
            if verb_text in verbs_unused:
                verbs_unused[verb_text].append(verb)
            else:
                verbs_unused[verb_text] = list()
                verbs_unused[verb_text].append(verb)

    # Adjectives
    adjectives_used = list()
    for adj in data[WordTypeEnum.ADJ]:
        adjectives_used.append(adj.txt)

    adj_query_string_statement = text("SELECT PosScore, NegScore, Adj_Key FROM adj")
    adjectives = conn.execute(adj_query_string_statement).fetchall()

    adjectives_unused = dict()
    for adj in adjectives:
        adj_text = adj.Adj_Key.lower().strip(Setting.NONWORD_CHARACTERS)
        if adj_text not in adjectives_used:
            if adj_text in adjectives_unused:
                adjectives_unused[adj_text].append(adj)
            else:
                adjectives_unused[adj_text] = list()
                adjectives_unused[adj_text].append(adj)

    return verbs_unused, adjectives_unused


# ưu tiên POS, nếu có nhiều POS thì lấy POS min, nếu không có POS sẽ lấy NEG min
def greedy_alg_1(data):
    verbs, adjectives = filter_word_list(data)
    additional_verbs = list()
    additional_adjectives = list()

    # verb
    for key_word, list_verb in verbs.items():

        if len(list_verb) == 1:
            # Chỉ có 1 lựa chọn, ưu tiên POS, nếu không có POS thì lấy NEG
            w_text = key_word
            w_type = WordTypeEnum.VERB

            if list_verb[0].PosScore > 0.0:
                w_kind = WordKindEnum.POS
                w_score = list_verb[0].PosScore
            else:
                w_kind = WordKindEnum.NEG
                w_score = (-1) * list_verb[0].NegScore

            verb_word = Word(w_text.strip(), w_score, w_kind, w_type)
            additional_verbs.append(verb_word)
        else:
            # Có nhiều hơn 1 lựa chọn, tìm MIN(POS), nếu MIN(POS) == 0, lấy MIN(NEG) || CHú ý là MIN phải khác 0
            # khởi tạo giá trị ban đầu
            verb_pos = list_verb[0]
            verb_neg = list_verb[0]

            # giá trị trong DB luôn dương
            min_pos = 0
            min_neg = 0

            # tìm giá trị hợp lệ đầu tiên
            for verb in list_verb:
                if verb.PosScore > 0:
                    min_pos = verb.PosScore
                    verb_pos = verb
                    break

            # tìm giá trị hợp lệ đầu tiên
            for verb in list_verb:
                if verb.NegScore > 0:
                    min_neg = verb.NegScore
                    verb_neg = verb
                    break

            for verb in list_verb:
                if 0 < verb.PosScore < min_pos:
                    min_pos = verb.PosScore
                    verb_pos = verb

                if 0 < verb.NegScore < min_neg:
                    min_neg = verb.NegScore
                    verb_neg = verb

            if min_pos > 0:
                verb_word = Word(verb_pos.SynsetTerm.strip(), verb_pos.PosScore, WordKindEnum.POS, WordTypeEnum.VERB)
            else:
                verb_word = Word(verb_neg.SynsetTerm.strip(), (-1) * verb_neg.NegScore, WordKindEnum.NEG, WordTypeEnum.VERB)

            additional_verbs.append(verb_word)

    # adjective
    for key_word, list_adjective in adjectives.items():

        if len(list_adjective) == 1:
            # Chỉ có 1 lựa chọn, ưu tiên POS, nếu không có POS thì lấy NEG
            w_text = key_word
            w_type = WordTypeEnum.VERB

            if list_adjective[0].PosScore > 0:
                w_kind = WordKindEnum.POS
                w_score = list_adjective[0].PosScore
            else:
                w_kind = WordKindEnum.NEG
                w_score = (-1) * list_adjective[0].NegScore

            adj_word = Word(w_text.strip(), w_score, w_kind, w_type)
            additional_adjectives.append(adj_word)
        else:
            # Có nhiều hơn 1 lựa chọn, tìm MIN(POS), nếu MIN(POS) == 0, lấy MIN(NEG)
            # khởi tạo giá trị ban đầu
            adj_pos = list_adjective[0]
            adj_neg = list_adjective[0]

            # giá trị trong DB luôn dương
            min_pos = 0
            min_neg = 0
            for adj in list_adjective:
                if adj.PosScore > 0:
                    min_pos = adj.PosScore
                    adj_pos = adj
                    break

            for adj in list_adjective:
                if adj.NegScore > 0:
                    min_neg = adj.NegScore
                    adj_neg = adj
                    break

            for adj in list_adjective:
                if 0 < adj.PosScore < min_pos:
                    min_pos = adj.PosScore
                    adj_pos = adj

                if 0 < adj.NegScore < min_neg:
                    min_neg = adj.NegScore
                    adj_neg = adj

            if min_pos > 0:
                adj_word = Word(adj_pos.Adj_Key.strip(), adj_pos.PosScore, WordKindEnum.POS, WordTypeEnum.ADJ)
            else:
                adj_word = Word(adj_neg.Adj_Key.strip(), (-1) * adj_neg.NegScore, WordKindEnum.NEG, WordTypeEnum.ADJ)

            additional_adjectives.append(adj_word)

    return additional_verbs, additional_adjectives


# ưu tiên POS, nếu có nhiều POS thì lấy POS max, nếu không có POS sẽ lấy NEG min
def greedy_alg_2(data):
    verbs, adjectives = filter_word_list(data)
    additional_verbs = list()
    additional_adjectives = list()

    # verb
    for key_word, list_verb in verbs.items():

        if len(list_verb) == 1:
            # Chỉ có 1 lựa chọn, ưu tiên POS, nếu không có POS thì lấy NEG
            w_text = key_word
            w_type = WordTypeEnum.VERB

            if list_verb[0].PosScore > 0.0:
                w_kind = WordKindEnum.POS
                w_score = list_verb[0].PosScore
            else:
                w_kind = WordKindEnum.NEG
                w_score = (-1) * list_verb[0].NegScore

            verb_word = Word(w_text.strip(), w_score, w_kind, w_type)
            additional_verbs.append(verb_word)
        else:
            # Có nhiều hơn 1 lựa chọn, tìm MAX(POS), nếu MAX(POS) == 0, lấy MIN(NEG) || CHú ý là MAX phải khác 0
            # khởi tạo giá trị ban đầu
            verb_pos = list_verb[0]
            verb_neg = list_verb[0]

            # giá trị trong DB luôn dương
            max_pos = 0
            min_neg = 0

            # tìm giá trị hợp lệ đầu tiên
            for verb in list_verb:
                if verb.PosScore > 0:
                    max_pos = verb.PosScore
                    verb_pos = verb
                    break

            # tìm giá trị hợp lệ đầu tiên
            for verb in list_verb:
                if verb.NegScore > 0:
                    min_neg = verb.NegScore
                    verb_neg = verb
                    break

            for verb in list_verb:
                if verb.PosScore > max_pos:
                    max_pos = verb.PosScore
                    verb_pos = verb

                if 0 < verb.NegScore < min_neg:
                    min_neg = verb.NegScore
                    verb_neg = verb

            if max_pos > 0:
                verb_word = Word(verb_pos.SynsetTerm.strip(), verb_pos.PosScore, WordKindEnum.POS, WordTypeEnum.VERB)
            else:
                verb_word = Word(verb_neg.SynsetTerm.strip(), (-1) * verb_neg.NegScore, WordKindEnum.NEG,
                                 WordTypeEnum.VERB)

            additional_verbs.append(verb_word)

    # adjective
    for key_word, list_adjective in adjectives.items():

        if len(list_adjective) == 1:
            # Chỉ có 1 lựa chọn, ưu tiên POS, nếu không có POS thì lấy NEG
            w_text = key_word
            w_type = WordTypeEnum.VERB

            if list_adjective[0].PosScore > 0:
                w_kind = WordKindEnum.POS
                w_score = list_adjective[0].PosScore
            else:
                w_kind = WordKindEnum.NEG
                w_score = (-1) * list_adjective[0].NegScore

            adj_word = Word(w_text.strip(), w_score, w_kind, w_type)
            additional_adjectives.append(adj_word)
        else:
            # Có nhiều hơn 1 lựa chọn, tìm MAX(POS), nếu MAX(POS) == 0, lấy MIN(NEG)
            # khởi tạo giá trị ban đầu
            adj_pos = list_adjective[0]
            adj_neg = list_adjective[0]

            # giá trị trong DB luôn dương
            max_pos = 0
            min_neg = 0
            for adj in list_adjective:
                if adj.PosScore > 0:
                    max_pos = adj.PosScore
                    adj_pos = adj
                    break

            for adj in list_adjective:
                if adj.NegScore > 0:
                    min_neg = adj.NegScore
                    adj_neg = adj
                    break

            for adj in list_adjective:
                if adj.PosScore > max_pos:
                    max_pos = adj.PosScore
                    adj_pos = adj

                if 0 < adj.NegScore < min_neg:
                    min_neg = adj.NegScore
                    adj_neg = adj

            if max_pos > 0:
                adj_word = Word(adj_pos.Adj_Key.strip(), adj_pos.PosScore, WordKindEnum.POS, WordTypeEnum.ADJ)
            else:
                adj_word = Word(adj_neg.Adj_Key.strip(), (-1) * adj_neg.NegScore, WordKindEnum.NEG, WordTypeEnum.ADJ)

            additional_adjectives.append(adj_word)

    return additional_verbs, additional_adjectives


# ưu tiên NEG, nếu có nhiều NEG thì lấy NEG max (số âm, gần 0 hơn), nếu không có NEG sẽ lấy POS min
def greedy_alg_3(data):
    verbs, adjectives = filter_word_list(data)
    additional_verbs = list()
    additional_adjectives = list()

    # verb
    for key_word, list_verb in verbs.items():

        if len(list_verb) == 1:
            # Chỉ có 1 lựa chọn, ưu tiên NEG, nếu không có NEG thì lấy POS
            w_text = key_word
            w_type = WordTypeEnum.VERB

            if list_verb[0].NegScore > 0.0:
                w_kind = WordKindEnum.NEG
                w_score = (-1) * list_verb[0].NegScore
            else:
                w_kind = WordKindEnum.POS
                w_score = list_verb[0].PosScore

            verb_word = Word(w_text.strip(), w_score, w_kind, w_type)
            additional_verbs.append(verb_word)
        else:
            # Có nhiều hơn 1 lựa chọn, tìm MIN(NEG), nếu MIN(NEG) == 0, lấy MIN(POS)
            # khởi tạo giá trị ban đầu
            verb_pos = list_verb[0]
            verb_neg = list_verb[0]

            # giá trị trong DB luôn dương
            min_pos = 0
            min_neg = 0

            # tìm giá trị hợp lệ đầu tiên
            for verb in list_verb:
                if verb.PosScore > 0:
                    min_pos = verb.PosScore
                    verb_pos = verb
                    break

            # tìm giá trị hợp lệ đầu tiên
            for verb in list_verb:
                if verb.NegScore > 0:
                    min_neg = verb.NegScore
                    verb_neg = verb
                    break

            for verb in list_verb:
                if 0 < verb.PosScore < min_pos:
                    min_pos = verb.PosScore
                    verb_pos = verb

                if 0 < verb.NegScore < min_neg:
                    min_neg = verb.NegScore
                    verb_neg = verb

            if min_neg > 0:
                verb_word = Word(verb_neg.SynsetTerm.strip(), (-1) * verb_neg.NegScore, WordKindEnum.NEG,
                                 WordTypeEnum.VERB)
            else:
                verb_word = Word(verb_pos.SynsetTerm.strip(), verb_pos.PosScore, WordKindEnum.POS, WordTypeEnum.VERB)

            additional_verbs.append(verb_word)

    # adjective
    for key_word, list_adjective in adjectives.items():

        if len(list_adjective) == 1:
            # Chỉ có 1 lựa chọn, ưu tiên NEG, nếu không có NEG thì lấy POS
            w_text = key_word
            w_type = WordTypeEnum.VERB

            if list_adjective[0].NegScore > 0:
                w_kind = WordKindEnum.NEG
                w_score = (-1) * list_adjective[0].NegScore
            else:
                w_kind = WordKindEnum.POS
                w_score = list_adjective[0].PosScore

            adj_word = Word(w_text.strip(), w_score, w_kind, w_type)
            additional_adjectives.append(adj_word)
        else:
            # Có nhiều hơn 1 lựa chọn, tìm MAX(NEG), nếu MAX(NEG) == 0, lấy MIN(POS)
            # khởi tạo giá trị ban đầu
            adj_pos = list_adjective[0]
            adj_neg = list_adjective[0]

            # giá trị trong DB luôn dương
            min_pos = 0
            min_neg = 0
            for adj in list_adjective:
                if adj.PosScore > 0:
                    min_pos = adj.PosScore
                    adj_pos = adj
                    break

            for adj in list_adjective:
                if adj.NegScore > 0:
                    min_neg = adj.NegScore
                    adj_neg = adj
                    break

            for adj in list_adjective:
                if 0 < adj.PosScore < min_pos:
                    min_pos = adj.PosScore
                    adj_pos = adj

                if 0 < adj.NegScore < min_neg:
                    min_neg = adj.NegScore
                    adj_neg = adj

            if min_neg > 0:
                adj_word = Word(adj_neg.Adj_Key.strip(), (-1) * adj_neg.NegScore, WordKindEnum.NEG, WordTypeEnum.ADJ)
            else:
                adj_word = Word(adj_pos.Adj_Key.strip(), adj_pos.PosScore, WordKindEnum.POS, WordTypeEnum.ADJ)

            additional_adjectives.append(adj_word)

    return additional_verbs, additional_adjectives


# ưu tiên NEG, nếu có nhiều NEG thì lấy NEG min, nếu không có NEG sẽ lấy POS min
def greedy_alg_4(data):
    verbs, adjectives = filter_word_list(data)
    additional_verbs = list()
    additional_adjectives = list()

    # verb
    for key_word, list_verb in verbs.items():

        if len(list_verb) == 1:
            # Chỉ có 1 lựa chọn, ưu tiên NEG, nếu không có NEG thì lấy POS
            w_text = key_word
            w_type = WordTypeEnum.VERB

            if list_verb[0].NegScore > 0.0:
                w_kind = WordKindEnum.NEG
                w_score = (-1) * list_verb[0].NegScore
            else:
                w_kind = WordKindEnum.POS
                w_score = list_verb[0].PosScore

            verb_word = Word(w_text.strip(), w_score, w_kind, w_type)
            additional_verbs.append(verb_word)
        else:
            # Có nhiều hơn 1 lựa chọn, tìm MIN(NEG), nếu MIN(NEG) == 0, lấy MIN(POS)
            # khởi tạo giá trị ban đầu
            verb_pos = list_verb[0]
            verb_neg = list_verb[0]

            # giá trị trong DB luôn dương
            min_pos = 0
            max_neg = 0

            # tìm giá trị hợp lệ đầu tiên
            for verb in list_verb:
                if verb.PosScore > 0:
                    min_pos = verb.PosScore
                    verb_pos = verb
                    break

            # tìm giá trị hợp lệ đầu tiên
            for verb in list_verb:
                if verb.NegScore > 0:
                    max_neg = verb.NegScore
                    verb_neg = verb
                    break

            for verb in list_verb:
                if 0 < verb.PosScore < min_pos:
                    min_pos = verb.PosScore
                    verb_pos = verb

                if verb.NegScore > max_neg:
                    max_neg = verb.NegScore
                    verb_neg = verb

            if max_neg > 0:
                verb_word = Word(verb_neg.SynsetTerm.strip(), (-1) * verb_neg.NegScore, WordKindEnum.NEG,
                                 WordTypeEnum.VERB)
            else:
                verb_word = Word(verb_pos.SynsetTerm.strip(), verb_pos.PosScore, WordKindEnum.POS, WordTypeEnum.VERB)

            additional_verbs.append(verb_word)

    # adjective
    for key_word, list_adjective in adjectives.items():

        if len(list_adjective) == 1:
            # Chỉ có 1 lựa chọn, ưu tiên NEG, nếu không có NEG thì lấy POS
            w_text = key_word
            w_type = WordTypeEnum.VERB

            if list_adjective[0].NegScore > 0:
                w_kind = WordKindEnum.NEG
                w_score = (-1) * list_adjective[0].NegScore
            else:
                w_kind = WordKindEnum.POS
                w_score = list_adjective[0].PosScore

            adj_word = Word(w_text.strip(), w_score, w_kind, w_type)
            additional_adjectives.append(adj_word)
        else:
            # Có nhiều hơn 1 lựa chọn, tìm MAX(NEG), nếu MAX(NEG) == 0, lấy MIN(POS)
            # khởi tạo giá trị ban đầu
            adj_pos = list_adjective[0]
            adj_neg = list_adjective[0]

            # giá trị trong DB luôn dương
            min_pos = 0
            max_neg = 0
            for adj in list_adjective:
                if adj.PosScore > 0:
                    min_pos = adj.PosScore
                    adj_pos = adj
                    break

            for adj in list_adjective:
                if adj.NegScore > 0:
                    max_neg = adj.NegScore
                    adj_neg = adj
                    break

            for adj in list_adjective:
                if 0 < adj.PosScore < min_pos:
                    min_pos = adj.PosScore
                    adj_pos = adj

                if adj.NegScore > max_neg:
                    max_neg = adj.NegScore
                    adj_neg = adj

            if max_neg > 0:
                adj_word = Word(adj_neg.Adj_Key.strip(), (-1) * adj_neg.NegScore, WordKindEnum.NEG, WordTypeEnum.ADJ)
            else:
                adj_word = Word(adj_pos.Adj_Key.strip(), adj_pos.PosScore, WordKindEnum.POS, WordTypeEnum.ADJ)

            additional_adjectives.append(adj_word)

    return additional_verbs, additional_adjectives


def greedy(data, alg=1):
    if alg == 2:
        return greedy_alg_2(data)
    elif alg == 3:
        return greedy_alg_3(data)
    elif alg == 4:
        return greedy_alg_4(data)
    else:
        return greedy_alg_1(data)


