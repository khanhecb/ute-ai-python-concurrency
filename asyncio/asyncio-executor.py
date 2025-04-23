#!/bin/python
#!/usr/bin/env python3
"""
Sort as a Service (SaaS) - ví dụ kết hợp AsyncIO và ProcessPoolExecutor
------------------------------------------------------------------------

Minh họa cách sử dụng vòng lặp sự kiện (event loop) của AsyncIO kết hợp với 
ProcessPoolExecutor để xử lý các tác vụ nặng CPU (blocking) một cách không đồng bộ (non-blocking).

Mặc dù việc cung cấp một "dịch vụ sắp xếp" là không thực tế,
nhưng ví dụ này cho thấy nhiều ý tưởng quan trọng trong lập trình song song với Python:
    - Tách biệt công việc nặng CPU sang tiến trình riêng (multiprocessing)
    - Viết mã async sạch sẽ, dễ hiểu
    - Tránh làm nghẽn vòng lặp sự kiện chính

Cách hoạt động:
    - Server nhận kết nối TCP
    - Nhận một danh sách số dưới dạng JSON (có kèm độ dài đầu gói tin)
    - Sắp xếp danh sách bằng thuật toán "Gnome sort"
    - Trả lại kết quả dưới dạng JSON

Để kiểm thử:
    1. Chạy server
    2. Gửi dữ liệu: [8 byte độ dài][chuỗi JSON danh sách số]
    (có thể dùng Python hoặc netcat làm client)
"""

import asyncio
import json
from concurrent.futures import ProcessPoolExecutor

def sort_in_process(data):
    nums = json.loads(data.decode())
    curr = 1 
    while curr < len(nums):
        if nums[curr] < nums[curr - 1]:
            curr += 1
        else:
            nums[curr], nums[curr -1] = \
                nums[curr - 1], nums[curr]
            if curr > 1:
                curr -= 1
    return json.dumps(nums).encode()

@asyncio.coroutine
def sort_request(reader, writer):
    print("Received connection")
    length = yield from reader.read(8)
    data = yield from reader.readexactly(
        int.from_bytes(length, 'big'))
    result = yield from asyncio.get_event_loop().run_in_executor(
        None, sort_in_process, data)
    print("Sorted list")
    writer.write(result)
    writer.close()
    print("Connection closed")

loop = asyncio.get_event_loop()
loop.set_default_executor(ProcessPoolExecutor())
server = loop.run_until_complete(
    asyncio.start_server(sort_request, '127.0.0.1', 2015))
print("Sort Service running")

loop.run_forever()
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()