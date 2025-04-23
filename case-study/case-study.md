## Case Study: Image Compression Tool

### Mục tiêu
Phần Case Study này xây dựng một công cụ nén ảnh đơn giản, tập trung vào việc nén các ảnh đen trắng (1 bit mỗi pixel, chỉ có trạng thái bật hoặc tắt) bằng kỹ thuật mã hóa độ dài chuỗi (run-length encoding - RLE). Công cụ sẽ:

- Nhận các ảnh đen trắng định dạng BMP (dễ đọc dữ liệu và có tiềm năng cải thiện kích thước tệp).
- Sử dụng RLE để nén dữ liệu, thay thế các chuỗi bit lặp lại bằng số lượng bit lặp lại (ví dụ: `000011000` thành `041203` để biểu thị 4 số 0, 2 số 1, rồi 3 số 0).
- Chia mỗi hàng ảnh thành các khối 127 bit để xử lý.
- Tận dụng các mô hình đồng thời (concurrency) để cải thiện hiệu suất, thử nghiệm các chiến lược khác nhau như thread pools và process pools.

### Lý do chọn ảnh đen trắng và RLE
Ảnh đen trắng là ứng cử viên tốt cho RLE vì chúng có xu hướng chứa các chuỗi bit dài giống nhau, giúp nén hiệu quả. Việc chia thành khối 127 bit được chọn vì:
- 127 giá trị có thể được mã hóa trong 7 bit, cho phép lưu trữ một hàng toàn 0 hoặc toàn 1 trong một byte duy nhất (bit đầu tiên chỉ màu, 7 bit còn lại chỉ số lượng).
- Các khối độc lập, cho phép xử lý song song mà không phụ thuộc lẫn nhau.

Tuy nhiên, việc chia khối có nhược điểm: nếu một chuỗi dài bị chia nhỏ, các chuỗi ngắn hơn có thể làm tăng kích thước tệp nén.

### Cấu trúc tệp nén
Tệp nén sẽ có định dạng:
- **2 byte đầu tiên**: Chiều rộng (width) của ảnh, lưu dưới dạng số nguyên 16-bit little-endian.
- **2 byte tiếp theo**: Chiều cao (height) của ảnh, lưu tương tự.
- **Phần còn lại**: Dữ liệu nén, bao gồm các byte biểu thị các khối 127 bit của mỗi hàng.

### Phân tích vấn đề: I/O-bound hay CPU-bound?
Tác giả thừa nhận không chắc liệu ứng dụng này là **I/O-bound** (giới hạn bởi đọc/ghi đĩa) hay **CPU-bound** (giới hạn bởi tính toán). Giả định ban đầu là CPU-bound do quá trình nén, nhưng việc truyền dữ liệu giữa các tiến trình (nếu dùng multiprocessing) có thể làm giảm lợi ích song song. Một giải pháp tối ưu có thể là viết extension bằng C hoặc Cython, nhưng ở đây, tác giả tập trung vào Python thuần.

### Thiết kế Bottom-Up
Ứng dụng được xây dựng theo cách **bottom-up design**, bắt đầu từ các thành phần nhỏ, độc lập, sau đó kết hợp chúng để thử nghiệm các mô hình đồng thời khác nhau.

#### 1. Hàm `compress_chunk`
Hàm này nén một khối 127 bit bằng RLE, sử dụng thư viện `bitarray` (cần cài đặt qua `pip install bitarray`) để thao tác với các bit riêng lẻ. `bitarray` giúp giảm kích thước dữ liệu khi truyền giữa các tiến trình so với danh sách boolean hoặc chuỗi byte.

```python
from bitarray import bitarray

def compress_chunk(chunk):
    compressed = bytearray()
    count = 1
    last = chunk[0]
    for bit in chunk[1:]:
        if bit != last:
            compressed.append(count | (128 * last))
            count = 0
            last = bit
        count += 1
    compressed.append(count | (128 * last))
    return compressed
```

**Giải thích**:
- **Input**: `chunk` là một `bitarray` chứa 127 bit (hoặc ít hơn nếu là phần cuối của hàng).
- **Output**: Một `bytearray` chứa dữ liệu nén.
- **Thuật toán**:
  - Theo dõi bit hiện tại (`last`) và đếm số lần lặp (`count`).
  - Khi gặp bit khác, tạo một byte: bit cao nhất (128) biểu thị màu (0 hoặc 1), 7 bit còn lại biểu thị số lượng.
  - Thêm byte cuối cho chuỗi cuối cùng.
- **Lưu ý**: Thuật toán đơn giản nhưng phức tạp để triển khai và gỡ lỗi, mất hai ngày để hoàn thiện.

#### 2. Hàm `compress_row`
Hàm này nén một hàng ảnh bằng cách chia thành các khối 127 bit và nén từng khối.

```python
def compress_row(row):
    compressed = bytearray()
    chunks = split_bits(row, 127)
    for chunk in chunks:
        compressed.extend(compress_chunk(chunk))
    return compressed
```

**Giải thích**:
- **Input**: `row` là một `bitarray` biểu thị một hàng của ảnh.
- **Output**: Một `bytearray` chứa dữ liệu nén của hàng.
- Chia hàng thành các khối bằng hàm `split_bits` (xem dưới).
- Nén từng khối và nối kết quả.

#### 3. Hàm `split_bits`
Hàm generator chia một chuỗi bit thành các khối có độ dài xác định (127 bit).

```python
def split_bits(bits, width):
    for i in range(0, len(bits), width):
        yield bits[i:i+width]
```

**Giải thích**:
- **Input**: `bits` (chuỗi bit), `width` (độ dài khối, thường là 127).
- **Output**: Generator trả về các khối bit.
- Cắt chuỗi bit từ vị trí `i` đến `i+width` mỗi lần.

#### 4. Hàm `compress_in_executor`
Hàm này bọc các hàm trên để chạy trong một executor (thread pool hoặc process pool), cho phép thử nghiệm cả hai mô hình đồng thời.

```python
def compress_in_executor(executor, bits, width):
    row_compressors = []
    for row in split_bits(bits, width):
        compressor = executor.submit(compress_row, row)
        row_compressors.append(compressor)
    compressed = bytearray()
    for compressor in row_compressors:
        compressed.extend(compressor.result())
    return compressed
```

**Giải thích**:
- **Input**: `executor` (thread hoặc process pool), `bits` (chuỗi bit của ảnh), `width` (chiều rộng ảnh).
- **Output**: `bytearray` chứa dữ liệu nén.
- Chia ảnh thành các hàng, gửi từng hàng vào executor để nén song song.
- Thu thập kết quả từ các future và nối chúng.

#### 5. Hàm `compress_image`
Hàm này tải ảnh BMP bằng thư viện `pillow` (cần cài đặt qua `pip install pillow`), chuyển đổi thành bit, và nén.

```python
from PIL import Image
import sys

def compress_image(in_filename, out_filename, executor=None):
    executor = executor if executor else ProcessPoolExecutor()
    with Image.open(in_filename) as image:
        bits = bitarray(image.convert('1').getdata())
        width, height = image.size
    compressed = compress_in_executor(executor, bits, width)
    with open(out_filename, 'wb') as file:
        file.write(width.to_bytes(2, 'little'))
        file.write(height.to_bytes(2, 'little'))
        file.write(compressed)

def single_image_main():
    in_filename, out_filename = sys.argv[1:3]
    # executor = ThreadPoolExecutor(4)
    executor = ProcessPoolExecutor()
    compress_image(in_filename, out_filename, executor)
```

**Giải thích**:
- **Input**: `in_filename` (đường dẫn ảnh đầu vào), `out_filename` (đường dẫn tệp nén), `executor` (tùy chọn).
- **Output**: Tệp nén.
- Tải ảnh, chuyển thành chế độ đen trắng (`convert('1')`), lấy dữ liệu pixel dưới dạng bit.
- Nén dữ liệu bằng `compress_in_executor`.
- Ghi chiều rộng, chiều cao và dữ liệu nén vào tệp.

### Thử nghiệm hiệu suất
Tác giả đã thử nghiệm nén một ảnh lớn (7200x5600 pixel) với hai loại executor:
- **ProcessPoolExecutor**: Mất khoảng **7.5 giây**.
- **ThreadPoolExecutor**: Mất khoảng **9 giây**.

**Kết luận**:
- ProcessPool nhanh hơn một chút do tận dụng nhiều CPU, nhưng lợi ích bị giảm bởi chi phí truyền dữ liệu (`bitarray` và `bytearray`) giữa các tiến trình.
- Với một ảnh duy nhất, multiprocessing chỉ mang lại cải thiện nhỏ.

### Mở rộng: Nén nhiều ảnh trong thư mục
Để tận dụng concurrency tốt hơn, tác giả mở rộng ứng dụng để nén tất cả ảnh BMP trong một thư mục, chỉ truyền tên tệp giữa các tiến trình (giảm chi phí truyền dữ liệu).

```python
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

def compress_dir(in_dir, out_dir):
    if not out_dir.exists():
        out_dir.mkdir(parents=True)
    executor = ProcessPoolExecutor()
    for file in (f for f in in_dir.iterdir() if f.suffix == '.bmp'):
        out_file = (out_dir / file.name).with_suffix('.rle')
        executor.submit(compress_image, str(file), str(out_file))

def dir_images_main():
    in_dir, out_dir = (Path(p) for p in sys.argv[1:3])
    compress_dir(in_dir, out_dir)
```

**Giải thích**:
- **Input**: `in_dir` (thư mục chứa ảnh BMP), `out_dir` (thư mục lưu tệp nén).
- Tạo thư mục đầu ra nếu chưa tồn tại.
- Sử dụng `ProcessPoolExecutor` để chạy `compress_image` cho mỗi ảnh trong thư mục.
- Mỗi `compress_image` lại tạo một `ProcessPoolExecutor` riêng để nén các hàng (tức là executor lồng nhau).

### So sánh hiệu suất với nhiều ảnh
Tác giả thử nghiệm bốn tổ hợp của thread và process pools:
- **ProcessPool cho mỗi ảnh + ProcessPool cho mỗi hàng**: 42 giây.
- **ProcessPool cho mỗi ảnh + ThreadPool cho mỗi hàng**: **34 giây** (nhanh nhất).
- **ThreadPool cho mỗi ảnh + ProcessPool cho mỗi hàng**: 53 giây.
- **ThreadPool cho mỗi ảnh + ThreadPool cho mỗi hàng**: 64 giây (chậm nhất).

**Phân tích**:
- Tổ hợp chậm nhất (ThreadPool + ThreadPool) là do GIL (Global Interpreter Lock) ngăn Python chạy song song thực sự.
- Tổ hợp nhanh nhất (ProcessPool + ThreadPool) hoạt động tốt vì:
  - Mỗi ảnh được xử lý trên một CPU riêng, chỉ truyền tên tệp (ít dữ liệu).
  - Trong mỗi tiến trình, việc nén hàng dùng ThreadPool tránh chi phí truyền dữ liệu giữa các tiến trình con, đặc biệt khi máy chỉ có 4 lõi CPU.
- Khi dùng ProcessPool cho cả ảnh và hàng, các tiến trình con cạnh tranh CPU, làm giảm hiệu suất.

**Kết luận**:
- Với nhiều ảnh, dùng ProcessPool cho mỗi ảnh và ThreadPool cho mỗi hàng là tối ưu.
- Với ảnh kích thước nhỏ, concurrency có thể không mang lại lợi ích đáng kể so với chạy tuần tự, vì thời gian xử lý đã đủ nhanh.

### Giải nén ảnh
Để kiểm tra thuật toán, tác giả cung cấp mã giải nén ảnh từ định dạng RLE về BMP.

```python
from PIL import Image
import sys

def decompress(width, height, bytes):
    image = Image.new('1', (width, height))
    row, col = 0, 0
    for byte in bytes:
        color = (byte & 128) >> 7
        count = byte & ~128
        for i in range(count):
            image.putpixel((row, col), color)
            row += 1
        if not row % width:
            col += 1
            row = 0
    return image

with open(sys.argv[1], 'rb') as file:
    width = int.from_bytes(file.read(2), 'little')
    height = int.from_bytes(file.read(2), 'little')
    image = decompress(width, height, file.read())
    image.save(sys.argv[2], 'bmp')
```

**Giải thích**:
- Đọc chiều rộng và chiều cao từ 4 byte đầu.
- Với mỗi byte trong dữ liệu nén:
  - Trích xuất màu (bit cao nhất) và số lượng (7 bit thấp).
  - Đặt các pixel tương ứng trong ảnh.
- Lưu ảnh giải nén dưới dạng BMP.
- **Lưu ý**: Tác giả thừa nhận mã này có thể còn lỗi và cần phát triển theo hướng test-driven để đảm bảo chính xác.

### Vai trò của AsyncIO
Tác giả đánh giá rằng **AsyncIO** có thể không phù hợp cho ứng dụng này vì:
- Hệ điều hành thường không hỗ trợ đọc/ghi tệp không chặn (non-blocking).
- AsyncIO sẽ phải bọc các thao tác I/O trong futures, làm mất lợi ích so với thread/process pools.

### Bài học rút ra
- **Concurrency phụ thuộc vào workload**: Với ảnh đơn lẻ, ProcessPool chỉ cải thiện nhẹ; với nhiều ảnh, ProcessPool cho ảnh và ThreadPool cho hàng là tốt nhất.
- **Truyền dữ liệu ảnh hưởng lớn**: Giảm dữ liệu truyền giữa tiến trình (như chỉ truyền tên tệp) cải thiện hiệu suất đáng kể.
- **Test-driven development**: Tác giả hối tiếc vì không dùng TDD, dẫn đến khó khăn trong việc phát hiện lỗi.
- **Chọn công cụ phù hợp**: Thread, process, hay AsyncIO đều có ưu/nhược điểm, cần thử nghiệm để tìm giải pháp tối ưu.

---

## Kết luận
Phần Case Study trong Chapter 13 minh họa cách áp dụng các mô hình đồng thời (futures với thread/process pools) vào một vấn đề thực tế: nén ảnh đen trắng. Nó nhấn mạnh tầm quan trọng của việc thử nghiệm các chiến lược khác nhau và hiểu bản chất I/O-bound hay CPU-bound của ứng dụng. Mặc dù ứng dụng không phức tạp, nó cung cấp cái nhìn sâu sắc về cách thiết kế và tối ưu hóa hệ thống đồng thời trong Python, đồng thời cảnh báo về những cạm bẫy như chi phí truyền dữ liệu và cạnh tranh tài nguyên.