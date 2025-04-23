# Asyncio Executor

---

## 🔧 **Sử dụng Executor để bao bọc mã blocking trong AsyncIO**

### 🎯 Vấn đề:
Trong `asyncio`, ta muốn mọi thứ đều **không chặn** (non-blocking) để tận dụng vòng lặp sự kiện (event loop). Tuy nhiên:
- Nhiều đoạn mã Python vẫn là **blocking** (gây nghẽn), ví dụ:
  - Hàm tính toán nặng (CPU-bound).
  - Gọi thư viện không hỗ trợ async.
  - Gọi hàm như `time.sleep()`, `json.loads()` với dữ liệu lớn.

=> Nếu để các đoạn này chạy trong event loop, toàn bộ chương trình sẽ bị “đứng hình”.

---

### ✅ Giải pháp: **Dùng Executor (ThreadPool/ProcessPool)**
- `asyncio` cho phép bạn chạy mã blocking trong **thread hoặc process riêng** bằng `run_in_executor()`.
- Cách này giúp bạn:
  - Tách đoạn blocking khỏi event loop chính.
  - **Kết hợp tốt giữa async (cho I/O) và multiprocessing (cho CPU)**.

---

### 💡 Ứng dụng: "Sorting as a Service"
Tác giả minh họa bằng cách tạo một **dịch vụ web đơn giản**, cho phép người dùng:
- Gửi một mảng số (dưới dạng JSON).
- Server nhận và dùng `ProcessPoolExecutor` để **sắp xếp mảng đó** ở tiến trình khác.

---

## 🤔 Nhưng... đây là một ý tưởng tệ

Tác giả châm biếm ý tưởng này là **ngớ ngẩn** (stupid), vì:
- Python đã có hàm `sorted()` rất nhanh.
- Gnome Sort là một thuật toán **rất chậm**.
- Tạo cả một service chỉ để sắp xếp là **thừa thãi**, không thực tế.

> ❗ Đây là một bài học về **tư duy phản biện**: Khi làm phần mềm, bạn không chỉ nên quan tâm “làm thế nào”, mà còn nên hỏi “có nên làm việc này không?”

---

## 👍 Nhưng có gì hay?

Mặc dù ý tưởng thì “ngu ngốc”, cách triển khai lại rất tốt:

### ✅ 1. Sử dụng `ProcessPoolExecutor` đúng cách
- Chạy sorting (CPU-bound) ở tiến trình riêng.
- Giúp event loop chính vẫn hoạt động trơn tru.

### ✅ 2. Truyền JSON dạng byte thay vì object Python
- Giảm chi phí serialization (pickle).
- Tăng hiệu suất truyền dữ liệu giữa các tiến trình.

### ✅ 3. Async code nhìn như sync
- Nhờ `await loop.run_in_executor(...)`, bạn có code dễ hiểu, dễ viết, không cần dùng nhiều callback hay lock.

---

## 📌 Kết luận:
> Việc bao bọc đoạn mã blocking bằng Executor là một **kỹ thuật quan trọng trong asyncio** – giúp bạn kết hợp linh hoạt giữa bất đồng bộ (cho I/O) và đa tiến trình (cho CPU).

Dù ví dụ "Sort as a Service" chỉ mang tính minh họa, nó vẫn thể hiện cách **thiết kế tốt trong async Python** – sạch sẽ, gọn gàng, hiệu quả.

---

Bạn muốn mình trích đoạn code cụ thể trong ví dụ này và giải thích dòng lệnh không? Mình có thể viết lại thành đoạn `.py` để bạn chạy thử.