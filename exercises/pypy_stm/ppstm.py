# Main Documentation: https://pypy.org/posts/2015/03/pypy-stm-251-released-1342113838236225773.html#!
# Dev Documentation: https://doc.pypy.org/en/latest/
# Code: https://doc.pypy.org/en/latest/stackless.html
# Install: sudo apt install pypy
# Run: pypy3 ppstm.py

from _continuation import continulet

def invoke(_, callable, arg):
    return callable(arg)

def bootstrap(c):
    # Vòng lặp chạy mãi ở độ sâu đệ quy thấp
    callable, arg = c.switch()
    while True:
        # Khởi tạo continulet mới và chuyển đổi
        to = continulet(invoke, callable, arg)
        callable, arg = c.switch(to=to)

c = continulet(bootstrap)
c.switch()

def recursive(n):
    if n == 0:
        return ("ok", n)
    if n % 200 == 0:
        prev = c.switch((recursive, n - 1))
    else:
        prev = recursive(n - 1)
    return (prev[0], prev[1] + 1)

print(recursive(999999))  # In ra ('ok', 999999)