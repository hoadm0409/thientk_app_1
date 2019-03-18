class Word:
    def __init__(self, txt, score, w_kind, w_type=None):
        self.txt = txt
        self.score = score
        self.kind = w_kind
        self.type = w_type

    def __repr__(self):
        return '{} - {} - {} - {}'.format(self.txt, self.score, self.kind, self.type)

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.txt, self.score, self.kind, self.type)
