from PIL import Image

def convert_jpg_to_bmp(input_path, output_path):
    """
    Chuyển đổi một ảnh JPG sang BMP.
    """
    img = Image.open("input.jpg")  
    img.convert("RGB").save("input.bmp")

def convert_png_to_bmp(input_path, output_path):
    """
    Chuyển đổi một ảnh PNG sang BMP.
    """
    img = Image.open("input.png")
    img.convert("RGB").save("input.bmp")

def convert_bmp_to_jpg(input_path, output_path, quality=90):
    """
    Chuyển đổi một ảnh BMP sang JPG.
    
    Args:
        input_path (str): Đường dẫn đến file BMP đầu vào.
        output_path (str): Đường dẫn để lưu file JPG đầu ra.
        quality (int): Chất lượng ảnh JPG (0-100, mặc định 90).
    """
    try:
        # Mở file BMP
        with Image.open(input_path) as img:
            # Chuyển sang mode RGB nếu cần (JPG yêu cầu RGB)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # Lưu file dưới dạng JPG
            img.save(output_path, 'JPEG', quality=quality)
        print(f"Đã chuyển đổi {input_path} sang {output_path}")
    except Exception as e:
        print(f"Lỗi khi chuyển đổi {input_path}: {e}")