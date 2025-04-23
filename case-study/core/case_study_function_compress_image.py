#!/bin/python3
# Author: KhanhECB
# Date: 23/4/2025

from PIL import Image
import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from bitarray import bitarray
from bitarray import bitarray

def compess_chunk(chunk):
    """
    Nén một khối 127 bit bằng RLE.
    """
    compressed = bytearray()
    count = 1
    last = chunk[0]
    
    # Kiểm tra phần tử đầu tiên
    for bit in chunk[1:]:  # Duyệt từ phần tử thứ 2 đến hết
        if bit != last:
            compressed.append(count | (128 * last))
            count = 0
            last = bit
        count += 1
    compressed.append(count | (128 * last))  # Ghi phần tử cuối cùng
    return compressed

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

def compress_image(in_filename, out_filename, executor=None):
    """
    Tải ảnh BMP từ in_file, nén ảnh và lưu vào out_file.
    """

    executor = executor if executor else ProcessPoolExecutor()

    with Image.open(in_filename) as image:
        image_bw = image.convert('1')  # Chuyển sang ảnh 1-bit đen trắng
        pixels = image_bw.getdata()
        bits = bitarray([1 if pixel else 0 for pixel in pixels])
        width, height = image.size

    compressed = compress_in_executor(executor, bits, width)

    with open(out_filename, 'wb') as file:
        file.write(width.to_bytes(2, 'little'))
        file.write(height.to_bytes(2, 'little'))
        file.write(compressed)

def single_image_main():
    in_filename, out_filename = sys.argv[1:3]
    executor = ProcessPoolExecutor()
    compress_image(in_filename, out_filename, executor)

def compress_dir(in_dir, out_dir):
    if not out_dir.exists():
        out_dir.mkdir(parents=True)
    executor = ProcessPoolExecutor()
    for file in (f for f in in_dir.iterdir() if f.suffix == '.bmp'):
        out_file = (out_dir / file.name).with_suffix('.rle')
        executor.submit(compress_image, str(file), str(out_file), executor)

def dir_images_main():
    in_dir, out_dir = (Path(p) for p in sys.argv[1:3])
    compress_dir(in_dir, out_dir)
