from threading import Thread

class InputReader(Thread):
    def run(self):
        # Hiển thị lời nhắc và chờ người dùng nhập vào
        self.line_of_text = input("Enter some text and press enter: ")

# Tạo và khởi chạy luồng nhập liệu
thread = InputReader()
thread.start()

count = 1
result = 1

# Trong khi luồng nhập liệu vẫn đang chạy (người dùng chưa nhập xong)
while thread.is_alive():
    result = count * count
    print("Calculated squares up to {} * {} = {}".format(count, count, result))
    count += 1

# Sau khi người dùng đã nhập xong, hiển thị văn bản đã nhập
print("While you typed '{}'".format(thread.line_of_text))