## Hướng Dẫn

*   Có:
    1.	Database danh sách từ + điểm số scoreW  từ có thể lặp lại với điểm số khác nhau
    2.	File danh sách từ + điểm số (scoreL): duy nhất
*   Cần:
    1.	Quét database
    2.  Lọc ra danh sách từ mới thỏa yêu cầu:
    3.  Mỗi từ có 1 điểm số duy nhất
    4.  Điểm số có được là điểm số sai khác bé nhất của scoreW với scoreL

## Setup

* Tạo Folder
            
            data
                |__ input
                        |__word_list.txt
                |__ output
            
            
* Setting DB: Trong file utilities/setting.py thay đổi thông số để connect DB
* Install venv, install packages **requirements.txt**