#!/bin/python3
# Author: KhanhECB
# Date: 23/4/2025
# Description: Decompress a compressed image file and save it as a BMP file.

import sys
from PIL import Image

def decompress(width, height, bytes):
    """
    Giải nén ảnh từ dữ liệu RLE và trả về ảnh PIL 1-bit.
    input_file: RLE bytes
    output_file: ảnh PIL 1-bit
    """
    image = Image.new('1', (width, height))
    x = 0
    y = 0
    for byte in bytes:
        color = 0 if ((byte & 128) >> 7) == 1 else 255  # Đảm bảo 0 là đen và 255 là trắng
        count = byte & 127
        for _ in range(count):
            image.putpixel((x, y), color)
            x += 1
            if x >= width:
                x = 0
                y += 1
    return image


def decompress_image(input_file, output_file):
    """
    Giải nén file RLE thành ảnh BMP.
    Args:
        input_file (str): Đường dẫn file RLE đầu vào.
        output_file (str): Đường dẫn file BMP đầu ra.
    """
    with open(input_file, 'rb') as file:
        width = int.from_bytes(file.read(2), 'little')
        height = int.from_bytes(file.read(2), 'little')
        bytes_data = file.read()
    image = decompress(width, height, bytes_data)
    image.save(output_file, 'BMP')