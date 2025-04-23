#!/bin/python
# Author: KhanhECB
# Date: 23/4/2025

from bitarray import bitarray

def compess_chunk(chunk):
    """
    Nén một khối 127 bit bằng RLE, sử dụng thư viện bitarray để thao tác với các bit riêng lẻ.
    bitarray giúp giảm kích thước dữ liệu khi
    truyền giữa các tiến trình so với danh sách boolean hoặc chuỗi byte.
    """
    comppressed = bytearray()
    count = 1
    last = chunk[0]
    for bit in chunk[1]:
        if bit != last:
            comppressed.append(count | (128 * last))
            count = 0
            last = bit
        count += 1
    comppressed.append(count | (128 * last))
    return comppressed


# Compress Row
def split_bits(bits, width):
    """
    Hàm này chia một mảng bit thành các khối có kích thước width.
    """
    for i in range(0, len(bits), width):
        yield bits[i:i + width]

def compress_row(row):
    """
    Hàm này nén một hàng ảnh bằng cách chia thành các khối 127 bit và nén từng khối.
    """

    compressed = bytearray()
    chunks = split_bits(row, 127)
    for chunk in chunks:
        compressed.extend(compess_chunk(chunk))
    return compressed

#  Compress Executor
def compress_in_executor(executor, bits, width):
    row_compressors = []
    for row in split_bits(bits, width):
        compressor = executor.submit(compress_row, row)
        row_compressors.append(compressor)
    compressed = bytearray()
    for compressor in row_compressors:
        compressed.extend(compressor.result())
    return compressed
