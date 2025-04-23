# UTE AI - Python Concurrency

## 1. Threads - Đa luồng

**Thread** Dùng để xử lý việc khác khi chờ I/O
**Tạo ra** Bằng cách kế thừa class Thread và override method run
**Ưu và nhược điểm**
 Ưu điểm        | Nhược điểm                                                                                                
----------------|-----------------------------------------------------------------------------------------------------------
 Dễ dùng        | Khó đồng bộ dữ liệu khi chia sẽ bộ nhớ                                                                    
 Chia sẻ bộ nhớ | Bị giới hạn bởi GIL (Global Interpreter Lock) khiến việc xử lý song song bằng nhiều CPU là không hiệu quả

## 2. Multiprocessing - Đa tiến trình

**Multiprocessing** Tạo ra tiến trình riêng biệt, vượt qua giới hạn GIL.
**Tương thích** Phù hợp với các tác vụ nặng về tính toán (CPU-bound)
**Hướng sử dụng** Dùng multiprocessing.Process hoặc multiprocessing.Pool
**Nhược điểm** Có chi phí cao do cần pickle/unpickle dữ liệu giữa các tiến trình

## 3. Futures - 
**Futures** Giao diện trừu tượng gói việc chạy tiến trình hoặc luồng và truy xuất kết quả sau.
**Sử dụng** Có thể dùng ThreadPoolExecutor hoặc ProcessPoolExecutor từ concurrent.futures.
**Ưu điểm** Giúp mã rõ ràng, dễ bảo trì hơn so với xử lý đồng thời truyền thống​

## 4. AsyncIO
**AsyncIO** Cách tiếp cận hiện đại trong Python để xử lý đồng thời, dựa trên coroutine và event loop.
**Tương thích** Phù hợp cho các ứng dụng I/O-bound như web servers, socket servers
**Sử dụng** Dùng async def, await, asyncio.run, asyncio.create_task, v.v.​
**Ưu điểm** Không tạo ra thread/process mới mà chạy đồng bộ bằng cách "tạm dừng" chờ sự kiện xảy ra (yield).

--- 
## 5. Case Study

**Mục tiêu** Viết chương trình nén ảnh trắng đen (1-bit) theo kỹ thuật Run-Length Encoding (RLE), và thử nghiệm các phương pháp đồng thời để tăng hiệu suất.
**Yêu cầu**
- Ảnh trắng đen được chia thành các dòng, mỗi dòng chia tiếp thành nhóm 127 bit.
- Mỗi nhóm 127 bit được nén bằng cách đếm số bit giống nhau liên tiếp và ghi thành byte (bit đầu là màu, 7 bit sau là số lượng).
- Sử dụng thư viện bitarray để thao tác với bit (gọn và hiệu quả hơn list[bool]).
- Tối ưu chương trình với concurrency, thử:
    - Nén từng dòng song song bằng multiprocessing.Pool.
    - Hoặc mỗi ảnh là một process.

**Gợi ý** Với ảnh nhỏ thì song song không có nhiều lợi ích; ảnh lớn hoặc xử lý nhiều ảnh thì mới thấy hiệu quả.

---
---
## 6. Exercises

1. Tìm hiểu các thư viện hổ trợ Concurrency
- execnet
- Parallel Python
- Cython
- PyPy-STM
- Gevent
- Cài đặt và chạy thử với ví dụ đơn giản để hiểu thêm lựa chọn ngoài threading và asyncio.
---
2. Viết lại ứng dụng Threading sang sử dụng Futures
- Chọn ứng dụng bạn đã viết trước đó (xử lý dữ liệu, nén file, đọc tệp, tải dữ liệu...).
- Viết lại bằng concurrent.futures.ThreadPoolExecutor.
- Sau đó thử lại với ProcessPoolExecutor → So sánh tốc độ.
---
3. Viết HTTP Server bằng AsyncIO
- Viết dịch vụ trả về HTML cơ bản khi nhận HTTP GET (có thể dùng asyncio + socket).
**- Gợi ý** HTTP GET là chuỗi ASCII như GET / HTTP/1.1\r\nHost: localhost\r\n\r\n.
---
4. Tạo race condition trong thread
- Tạo biến toàn cục và cập nhật nó từ nhiều thread.
- In kết quả sau mỗi lần cập nhật để thấy sự “xung đột” và sai lệch dữ liệu.
---
5. Nâng cấp “link collector” (từ Chapter 6)
- Làm cho chương trình thu thập liên kết web chạy song song.
- So sánh 3 cách: raw thread, futures, và AsyncIO.
---
6. Viết lại tool nén RLE bằng concurrency
- Dùng thread hoặc process để xử lý từng dòng hoặc từng ảnh.
- Ghi nhận tốc độ xử lý & độ dễ bảo trì mã nguồn.