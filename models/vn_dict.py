class VNDict:
    __instance = None

    @staticmethod
    def get_instance():
        if VNDict.__instance is None:
            VNDict()
        return VNDict.__instance

    def __init__(self):
        if VNDict.__instance is not None:
            raise Exception('Something went wrong!')
        else:
            self.data_dict = {
                        'a': [],
                        'á': [],
                        'à': [],
                        'ả': [],
                        'ã': [],
                        'ạ': [],
                        'ă': [],
                        'ắ': [],
                        'ằ': [],
                        'ẳ': [],
                        'ẵ': [],
                        'ặ': [],
                        'â': [],
                        'ấ': [],
                        'ầ': [],
                        'ẩ': [],
                        'ẫ': [],
                        'ậ': [],
                        'b': [],
                        'c': [],
                        'd': [],
                        'đ': [],
                        'e': [],
                        'é': [],
                        'è': [],
                        'ẻ': [],
                        'ẽ': [],
                        'ẹ': [],
                        'ê': [],
                        'ế': [],
                        'ề': [],
                        'ể': [],
                        'ễ': [],
                        'ệ': [],
                        'f': [],
                        'g': [],
                        'h': [],
                        'i': [],
                        'í': [],
                        'ì': [],
                        'ỉ': [],
                        'ĩ': [],
                        'ị': [],
                        'j': [],
                        'k': [],
                        'l': [],
                        'm': [],
                        'n': [],
                        'o': [],
                        'ó': [],
                        'ò': [],
                        'ỏ': [],
                        'õ': [],
                        'ọ': [],
                        'ô': [],
                        'ố': [],
                        'ồ': [],
                        'ổ': [],
                        'ỗ': [],
                        'ộ': [],
                        'ơ': [],
                        'ớ': [],
                        'ờ': [],
                        'ở': [],
                        'ỡ': [],
                        'ợ': [],
                        'p': [],
                        'q': [],
                        'r': [],
                        's': [],
                        't': [],
                        'u': [],
                        'ú': [],
                        'ù': [],
                        'ủ': [],
                        'ũ': [],
                        'ụ': [],
                        'ư': [],
                        'ứ': [],
                        'ừ': [],
                        'ử': [],
                        'ữ': [],
                        'ự': [],
                        'v': [],
                        'w': [],
                        'x': [],
                        'y': [],
                        'ý': [],
                        'ỳ': [],
                        'ỷ': [],
                        'ỹ': [],
                        'ỵ': [],
                        '0': [],
                        '1': [],
                        '2': [],
                        '3': [],
                        '4': [],
                        '5': [],
                        '6': [],
                        '7': [],
                        '8': [],
                        '9': []
                    }
            VNDict.__instance = self

    def add(self, word):
        try:
            self.data_dict[word.txt[0]].append(word)
        except:
            print(word)

    def look_up(self, txt, w_kind=None, w_type=None):
        branch = []
        try:
            branch = self.data_dict[txt[0]]
        except:
            print('exception: ' + txt)

        words = list()

        for word in branch:
            if word.txt == txt:
                words.append(word)

        # filter by kind
        if w_kind is not None:
            words = [w for w in words if w.kind == w_kind]

        # filter by type
        if w_type is not None:
            words = [w for w in words if w.type == w_type]

        return words
