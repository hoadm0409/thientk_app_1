"""
    1: ưu tiên POS, nếu có nhiều POS thì lấy POS min, nếu không có POS sẽ lấy NEG min
    2: ưu tiên POS, nếu có nhiều POS thì lấy POS max, nếu không có POS sẽ lấy NEG min
    3: ưu tiên NEG, nếu có nhiều NEG thì lấy NEG max (số âm, gần 0 hơn), nếu không có NEG sẽ lấy POS min
    4: ưu tiên NEG, nếu có nhiều NEG thì lấy NEG min, nếu không có NEG sẽ lấy POS min
"""
GREEDY_1 = 1
GREEDY_2 = 2
GREEDY_3 = 3
GREEDY_4 = 4


class Setting:
    # Database
    # Thông tin kết nối DB chưa DB của từ điển.
    DB_HOST = 'localhost'
    DB_PORT = 3306
    DB_NAME = 'thientk'
    DB_USER = 'root'
    DB_PASSWORD = 'hoadinh'

    # Preprocess
    # các kí tự dưới đây đứng đầu hoặc cuối chuỗi sẽ bị loại bỏ
    NONWORD_CHARACTERS = ' ().,:"=>\\_-'

    # Greedy
    # Nếu chức năng này được bật, các words trong từ điển không xuất hiện
    # trong input data sẽ được thêm vào, dựa trên thuật toán được lwja chọn.
    # Thứ tự ưu tiên được mô tả phía trên, nếu độ ưu tiên không được mô tả.
    # Option GREEDY_1 sẽ được chọn làm mặc định.
    GREEDY = True
    GREEDY_ALGORITHMS = GREEDY_4

