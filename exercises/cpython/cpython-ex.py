# Install: pip install Cython
# Docx: https://cython.readthedocs.io/en/latest/src/userguide/parallelism.html

import cython
from cython.parallel import prange

i = cython.declare(cython.int)
n = cython.declare(cython.int, 10)
sum = cython.declare(cython.int, 0)

for i in prange(n, nogil=True):
    sum += i

print(sum)
