import os
from pdf2image import convert_from_path
from django.conf import settings
from PIL import Image

def convert_pdf_to_images(pdf_path, output_folder=None):
    if output_folder is None:
        output_folder = os.path.join(settings.MEDIA_ROOT, 'temp_images')
        os.makedirs(output_folder, exist_ok=True)
    
    images = convert_from_path(pdf_path)
    image_paths = []
    
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'page_{i+1}.jpg')
        image.save(image_path, 'JPEG')
        image_paths.append(image_path)
    
    return image_paths

def cleanup_temp_files(file_paths):
    for path in file_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Error deleting file {path}: {e}")