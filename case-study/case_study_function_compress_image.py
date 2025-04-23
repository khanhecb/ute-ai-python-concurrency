#!/bin/python3
# Author: KhanhECB
# Date: 23/4/2025

from PIL import Image
import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from case_study_function_compress import *

def compress_image(in_filename, out_filename, executor=None):
    """
    Tải ảnh BMP từ in_file, nén ảnh và lưu vào out_file.
    """

    executor = executor if executor else ProcessPoolExecutor()
    with Image.open(in_filename) as image:
        bits = bitarray(image.convert('1').getdata())
        width, height = image.size

    compressed = compress_in_executor(executor, bits, width)

    with open (out_filename, 'wb') as file:
        file.write(width.to_bytes(2, 'little'))
        file.write(height.to_bytes(2, 'little'))
        file.write(compressed)

def single_image_main():
    in_filename, out_filename = sys.argv[1:3]
    #executor = ThreadPoolExecutor(4)
    executor = ProcessPoolExecutor()
    compress_image(in_filename, out_filename, executor)

def compress_dir(in_dir, out_dir):
    if not out_dir.exists():
        out_dir.mkdir(parents=True)
    executor = ProcessPoolExecutor()
    for file in (f for f in in_dir.iterdir() if f.suffix == '.bmp'):
        out_file = (out_dir / file.name).with_suffix('.rle')
        executor.submit(compress_image, str(file), str(out_file))

def dir_images_main():
    in_dir, out_dir = (Path(p) for p in sys.argv[1:3])
    compress_dir(in_dir, out_dir)