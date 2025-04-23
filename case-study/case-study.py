#!/bin/python3
# Author: KhanhECB
# Date: 24/4/2025
# Description: Convert JPG to BMP, compress BMP to RLE, and decompress RLE to BMP 

from core import case_study_function_compress_image as compress_image
from core import case_study_function_decompress_image as decompress_image
from core import convert_image

result_folder_path = "result"

# Convert JPG to BMP
convert_image.convert_jpg_to_bmp("input.jpg", "input.bmp")

# Convert BMP to RLE
compress_image.compress_image("input.bmp", "input.rle")

# Decompress RLE to BMP
decompress_image.decompress_image("input.rle", "output.bmp")