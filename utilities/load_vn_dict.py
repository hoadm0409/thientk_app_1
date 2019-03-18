from utilities import get_db_connect_string
from models import VNDict, Word, WordKindEnum, WordTypeEnum
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from utilities import Setting


def load_vn_dict():
    # setting DB
    engine = create_engine(get_db_connect_string())
    conn = engine.connect()

    vn_dict = VNDict.get_instance()

    # load verbs
    verb_query_string_statement = text("SELECT PosScore, NegScore, SynsetTerm FROM verb")
    verbs = conn.execute(verb_query_string_statement).fetchall()

    for v in verbs:
        if v.PosScore > v.NegScore:
            word_score = v.PosScore
            word_kind = WordKindEnum.POS
        else:
            word_score = v.NegScore
            word_kind = WordKindEnum.NEG

        word_type = WordTypeEnum.VERB
        word_text = v.SynsetTerm.lower().strip(Setting.NONWORD_CHARACTERS)

        verb_w = Word(word_text, word_score, word_kind, word_type)
        vn_dict.add(verb_w)

    # load adjectives
    adj_query_string_statement = text("SELECT PosScore, NegScore, Adj_Key FROM adj")
    adjectives = conn.execute(adj_query_string_statement).fetchall()

    for adj in adjectives:
        if adj.PosScore > adj.NegScore:
            word_score = adj.PosScore
            word_kind = WordKindEnum.POS
        else:
            word_score = adj.NegScore
            word_kind = WordKindEnum.NEG

        word_type = WordTypeEnum.ADJ
        word_text = adj.Adj_Key.lower().strip(Setting.NONWORD_CHARACTERS)

        adj_w = Word(word_text, word_score, word_kind, word_type)
        vn_dict.add(adj_w)

