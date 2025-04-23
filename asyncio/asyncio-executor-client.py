import asyncio
import json

async def send_and_sort(numbers):
    reader, writer = await asyncio.open_connection('127.0.0.1', 2015)

    # Chuyển danh sách thành chuỗi JSON, sau đó thành bytes
    data = json.dumps(numbers).encode('utf-8')

    # Gửi 8 byte đầu tiên là độ dài của dữ liệu, dùng big-endian
    writer.write(len(data).to_bytes(8, byteorder='big'))

    # Gửi nội dung JSON
    writer.write(data)

    # Đảm bảo đã gửi xong
    await writer.drain()

    # Nhận phản hồi từ server (đã được sort)
    response = await reader.read()
    result = json.loads(response.decode('utf-8'))

    print(f"Kết quả từ server: {result}")

    writer.close()
    await writer.wait_closed()

# Danh sách ví dụ
numbers = [5, 9, 2, 7, 3, 8, 1, 4]

# Gọi hàm chính
asyncio.run(send_and_sort(numbers))
