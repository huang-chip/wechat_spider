import os
import requests
from PIL import Image
from io import BytesIO
import hashlib

class ImageProcessor:
    def __init__(self, image_dir='output/images'):
        self.image_dir = image_dir
        os.makedirs(image_dir, exist_ok=True)

    def download_and_compress(self, image_url, alt_text=''):
        try:
            # 下载图片
            response = requests.get(image_url)
            if response.status_code != 200:
                return None

            # 生成文件名
            file_hash = hashlib.md5(image_url.encode()).hexdigest()
            file_name = f"{file_hash}.jpg"
            file_path = os.path.join(self.image_dir, file_name)

            # 打开图片
            img = Image.open(BytesIO(response.content))

            # 转换为RGB模式(处理PNG等格式)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # 压缩图片
            self.compress_image(img, file_path, max_size_kb=300)

            return {
                'file_name': file_name,
                'file_path': file_path,
                'alt_text': alt_text
            }

        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return None

    def compress_image(self, img, output_path, max_size_kb=300, quality=95):
        """压缩图片到指定大小"""
        while quality > 5:
            # 调整图片尺寸
            max_size = (1920, 1920)  # 最大尺寸
            img.thumbnail(max_size, Image.LANCZOS)

            # 保存图片
            img.save(output_path, 'JPEG', quality=quality, optimize=True)

            # 检查文件大小
            file_size = os.path.getsize(output_path) / 1024  # 转换为KB
            if file_size <= max_size_kb:
                break

            # 如果文件仍然过大，降低质量继续尝试
            quality -= 5