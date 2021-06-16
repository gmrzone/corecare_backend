import os
from django.utils.text import slugify
from io import BytesIO
from PIL import Image, ImageFilter
import sys

def EmployeeIconLocation(instance, filename):
    path = os.path.join('Employee Category', instance.number, filename)
    return path

def SubcategoryIconLocation(instance, filename):
    path = os.path.join('Service SubCategory Images', slugify(instance.name), filename)
    return path

def SubcategoryPlaceholderLocation(instance, filename):
    path = os.path.join('Service SubCategory Placeholders', slugify(instance.name), f"placeholder_{filename}")
    return path

def ServiceIconLocation(instance, filename):
    path = os.path.join('Service Images', slugify(instance.name), filename)
    return path

def generate_placeholder(image, height):
    image_file = BytesIO()
    image_name = image.name
    pil_image = Image.open(image)
    content_type = Image.MIME[pil_image.format]
    ratio = height / pil_image.size[1]
    width = int(pil_image.size[0] * ratio)
    resized_image = pil_image.resize((width, height))
    blurred_image = resized_image.filter(ImageFilter.GaussianBlur(5))
    blurred_image.save(image_file, pil_image.format, quality=50)
    image_file.seek(0)
    file_size = sys.getsizeof(image_file)
    return image_file, image_name, file_size, content_type



