# Hướng dẫn Bài tập Chapter 13 - Lập trình Đồng thời trong Python

Chào cả nhóm! Phần bài tập (Exercises) của Chapter 13 là cơ hội để chúng ta cùng "đào sâu" vào lập trình đồng thời trong Python, từ threads, multiprocessing đến AsyncIO. Các bài tập này giúp nhóm hiểu cách áp dụng các công cụ đồng thời, so sánh hiệu suất, và xử lý các vấn đề thực tế như thu thập dữ liệu web hay nén dữ liệu. Tài liệu này tóm tắt các yêu cầu, mục tiêu, và gợi ý cách phân công công việc để nhóm hoàn thành hiệu quả.

## 1. Mục tiêu chung

- **Hiểu công cụ đồng thời**: Làm quen với threads, multiprocessing, futures, AsyncIO, và biết khi nào dùng cái nào.
- **Thực hành và so sánh**: Thử nghiệm các phương pháp, đo hiệu suất, và đánh giá độ phức tạp mã.
- **Ứng dụng thực tế**: Áp dụng vào các vấn đề như thu thập link web, mã hóa dữ liệu, hoặc xử lý lỗi đồng thời (race conditions).
- **Làm việc nhóm**: Phân chia nhiệm vụ, thảo luận kết quả, và cùng rút kinh nghiệm.

## 2. Tóm tắt các bài tập

### a. Khám phá thư viện bên thứ ba

- **Yêu cầu**: Tìm hiểu các thư viện như `execnet` (đồng thời không chia sẻ tài nguyên), `Parallel Python` (luồng song song), `Cython` (bỏ GIL), `PyPy-STM` (bộ nhớ giao dịch), và `Gevent` (hỗ trợ I/O-bound).
- **Mục tiêu**: Mở rộng kiến thức về các công cụ đồng thời ngoài chuẩn Python.
- **Gợi ý phân công**:
  - Mỗi thành viên chọn một thư viện, thử viết đoạn mã mẫu (ví dụ: tải web với `Gevent`).
  - Nhóm họp lại, trình bày cách thư viện hoạt động và so sánh ưu/nhược điểm.

### b. So sánh threads và futures

- **Yêu cầu**: Viết mã dùng `threading` cho một tác vụ (như tính tổng bình phương), rồi chuyển sang `concurrent.futures` (`ThreadPoolExecutor` hoặc `ProcessPoolExecutor`). So sánh thời gian chạy và tính dễ đọc.
- **Mục tiêu**: Hiểu tại sao futures gọn gàng hơn và khi nào cần multiprocessing để dùng nhiều CPU.
- **Gợi ý phân công**:
  - Một người viết mã threads, một người viết futures, một người đo thời gian và ghi nhận.
  - Thảo luận nhóm: Futures có giảm lỗi không? Multiprocessing có nhanh hơn đáng kể không?

### c. Xây dựng dịch vụ HTTP với AsyncIO

- **Yêu cầu**: Dùng `aiohttp` tạo server HTTP đơn giản, xử lý yêu cầu GET (ví dụ: trả về "Hello" trên trình duyệt).
- **Mục tiêu**: Nắm cách AsyncIO quản lý tác vụ mạng hiệu quả.
- **Gợi ý phân công**:
  - Một người nghiên cứu cấu trúc HTTP và viết mã server.
  - Một người kiểm tra server bằng trình duyệt, đảm bảo trả về đúng.
  - Nhóm thảo luận: AsyncIO có dễ dùng hơn threads cho mạng không?

### d. Tạo và hiểu race conditions

- **Yêu cầu**: Viết chương trình để nhiều luồng cập nhật biến chung (như bộ đếm), gây lỗi race condition (dữ liệu sai lệch).
- **Mục tiêu**: Hiểu vấn đề khi luồng truy cập dữ liệu chia sẻ và cách khắc phục (dùng `Lock`).
- **Gợi ý phân công**:
  - Một người viết mã gây lỗi race condition.
  - Một người thêm `Lock` để sửa lỗi, so sánh kết quả.
  - Nhóm thảo luận: Race conditions thường gặp ở đâu trong dự án thực tế?

### e. Tăng tốc thu thập liên kết web

- **Yêu cầu**: Cải thiện tool thu thập liên kết (từ Chương 6) bằng cách gửi yêu cầu HTTP song song, thử threads, futures, hoặc AsyncIO. So sánh tốc độ.
- **Mục tiêu**: Tìm phương pháp tối ưu cho tác vụ I/O-bound.
- **Gợi ý phân công**:
  - Chia nhóm: mỗi người thử một cách (threads, futures, AsyncIO).
  - Một người tổng hợp thời gian chạy và viết báo cáo so sánh.
  - Thảo luận: AsyncIO có vượt trội hơn trong trường hợp này không?

### f. Mã hóa độ dài chuỗi với đồng thời

- **Yêu cầu**: Viết lại mã hóa độ dài chuỗi (run-length encoding) bằng threads hoặc multiprocessing. Kiểm tra tốc độ, tính dễ đọc, và thử tăng tốc giải nén.
- **Mục tiêu**: Đánh giá lợi ích của đồng thời trong xử lý dữ liệu.
- **Gợi ý phân công**:
  - Một người viết mã tuần tự, một người dùng threads, một người dùng multiprocessing.
  - Một người đo thời gian và so sánh độ phức tạp mã.
  - Nhóm thảo luận: Có đáng dùng đồng thời cho tác vụ này không?

## 3. Hướng dẫn thực hiện

- **Công cụ cần cài**:
  ```bash
  pip install aiohttp
  ```
- **Cách đo hiệu suất**: Dùng `time.time()` hoặc `time.perf_counter()` để đo thời gian chạy của mỗi phương pháp.
- **Tài liệu tham khảo**:
  - Tài liệu Python về `threading`, `multiprocessing`, `concurrent.futures`, `asyncio`.
  - Hướng dẫn `aiohttp` cho server HTTP.
- **Phân công công việc**:
  - Mỗi bài tập chia thành các nhiệm vụ nhỏ (viết mã, đo thời gian, báo cáo).
  - Gặp nhau sau mỗi bài để chia sẻ kết quả, rút kinh nghiệm.
- **Ứng dụng thực tế**: Các bài tập này có thể áp dụng vào dự án AI (như thu thập dữ liệu web) hoặc tối ưu thuật toán xử lý dữ liệu.

## 4. Lời nhắn cho nhóm

Cả nhóm ơi, đây là cơ hội để chúng ta cùng "bung xõa" với lập trình đồng thời! Hãy chia nhiệm vụ công bằng, hỗ trợ nhau khi gặp lỗi (nhất là race conditions, dễ đau đầu lắm). Sau khi xong, ngồi lại chia sẻ xem cách nào hay nhất, học được gì, và có thể áp dụng vào dự án sau không. Chốt lại, làm bài tập này không chỉ để hiểu code mà còn để teamwork đỉnh hơn nha!

---