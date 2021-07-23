import os
import sys
from io import BytesIO

from django.utils.text import slugify
from PIL import Image, ImageFilter


def EmployeeIconLocation(instance, filename):
    path = os.path.join("Employee Category", instance.number, filename)
    return path


def SubcategoryIconLocation(instance, filename):
    path = os.path.join("Service SubCategory Images", slugify(instance.name), filename)
    return path


def SubcategoryPlaceholderLocation(instance, filename):
    path = os.path.join(
        "Service SubCategory Placeholders",
        slugify(instance.name),
        f"placeholder_{filename}",
    )
    return path


def ServiceIconLocation(instance, filename):
    path = os.path.join("Service Images", slugify(instance.name), filename)
    return path


def ServicePlaceholderLocation(instance, filename):
    path = os.path.join(
        "Service Placeholders", slugify(instance.name), f"placeholder{filename}"
    )
    return path


def generate_placeholder(image, blur: int, height: int, quality: int) -> tuple:
    image_file = BytesIO()
    image_name = image.name
    pil_image = Image.open(image)
    content_type = Image.MIME[pil_image.format]
    ratio = height / pil_image.size[1]
    width = int(pil_image.size[0] * ratio)
    resized_image = pil_image.resize((width, height))
    blurred_image = resized_image.filter(ImageFilter.GaussianBlur(blur))
    blurred_image.save(image_file, pil_image.format, quality=quality)
    image_file.seek(0)
    file_size = sys.getsizeof(image_file)
    return image_file, image_name, file_size, content_type
