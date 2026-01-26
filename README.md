# wplace_scraper

Bản sửa đổi của https://github.com/benjamin-lowry/wplacescrape.

## Hướng dẫn

### Cài đặt

1. Cài đặt Python về máy tính. Khuyên dùng Python 3.11 trở lên. 
2. Cài đặt các thư viện cần thiết: `pip install aiohttp xxhash`.
3. Tải mã nguồn chương trình.
Cách 1: Chọn nút *Code* màu xanh lục, rồi chọn *Download ZIP*. Sau khi tải xong thì giải nén ra 1 thư mục.
Cách 2 (nếu có git): `git clone https://github.com/benjamin-lowry/wplacescrape.git`

### Cấu hình

Mặc định, chương trình sẽ cào trong khu vực Việt Nam và biển Đông. Do quét theo hình chữ nhật nên sẽ có cả một phần của Lào và Campuchia.

Để thay đổi, mở tệp `config.py` và chỉnh sửa các hằng số cơ bản sau:
* `FROM_X`: bắt đầu cào từ tấm thứ bao nhiêu theo chiều ngang.
* `FROM_Y`: như `FROM_X`, nhưng là theo chiều dọc
* `TO_X`: kết thúc của `FROM_X`
* `TO_Y`: kết thúc của `FROM_Y`
Để lấy vị trí tấm (tile), vào wplace.live, chọn 1 điểm ảnh (pixel) bất kì, sẽ thấy *Tl X* và *Tl Y* là 2 toạ độ vị trí của tấm đó.

Mở tệp `index.htm`, tìm đến chỗ có `timeInterval` bên trong `timeDimensionOptions`, đặt thành khoảng thời gian mà dữ liệu của bạn xem được. 

### Cào dữ liệu
Mỗi ngày, hãy chạy tệp `archive.py` một lần. Nếu thấy dòng `Deleted <số> tiles.` và chương trình kết thúc là thành công. Một thư mục tên là `tiles` sẽ chứa tất cả dữ liệu ảnh. Nếu bị lỗi gì đó mà không biết sửa thì hãy xoá thư mục của ngày hôm nay (bên trong `tiles`) đi và chạy lại.

### Xem dữ liệu
Sau khi cào xong (lần đầu hay hôm sau), sẽ xuất hiện 1 tệp tên là `tile_availability.js`. Nếu không có tệp này thì không xem được bản đồ.

Mở tệp `index.htm` bằng trình duyệt bất kì. Giao diện bản đồ sẽ xuất hiện như sau:
[chưa có hình]

*(Để đổi toạ độ ban đầu, hãy sửa hằng số `START_COORDS` trong tệp `index.htm`)*

Các tính năng thì cũng như bản đồ thông thường thôi. Nếu đã cào được nhiều ngày thì có thể dùng thanh trượt thời gian để xem ở các mốc khác nhau.

Bạn có thể dùng OBS hoặc ShareX để tạo ảnh/video thời gian trôi (timelapse).

## Trợ giúp
Để báo lỗi và đề xuất tính năng, hãy vào phần [Issues](https://github.com/IoeCmcomc/wplace_scraper/issues "Issues"). Nếu có những thắc mắc liên quan đến chương trình, hãy vào mục [Discussions](https://github.com/IoeCmcomc/wplace_scraper/discussions "Discussions").

## Lời từ chối trách nhiệm
Phần mềm được tạo ra với sự hỗ trợ của mô hình ngôn ngữ lớn.

Nội dung do bạn cào từ Wplace về thuộc sở hữu của trang web đó và những người đóng góp.

Phần mềm này và tôi không liên kết hoặc quen biết với wplace.live.

## Giấy phép

Bản quyền 2025 Benjamin Lowry,
Bản quyền 2025-2026 IoeCmcomc

Phần mềm được phát hành dưới giấy phép Apache 2.0.