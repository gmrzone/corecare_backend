from api.utils import generate_placeholder
from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save
from .models import Post
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image, ImageFilter
from io import BytesIO
import sys
def get_post_placeholder_helper(instance, blur, height, quality):
    image_file, image_name, file_size, content_type = generate_placeholder(instance.photo, blur, height, quality)
    instance.placeholder = InMemoryUploadedFile(image_file, field_name="placeholder", name=image_name, size=file_size, content_type=content_type, charset="utf-8")

def optimize_images(instance, placeholder_blur, placeholder_height, placeholder_quality):
    instance_image = instance.photo
    image_name = instance_image.name
    image = Image.open(instance_image)
    image_format = image.format
    content_type = Image.MIME[image_format]
    max_height = 500
    if image.size[1] > 500:
        ratio = max_height / image.size[1]
        width = int(image.size[0] * ratio)
        image = image.resize((width, max_height))
    placeholder_ratio = placeholder_height / image.size[1]
    placeholder_width = int(image.size[0] * placeholder_ratio)
    placeholder_image = image.resize((placeholder_width, placeholder_height))
    placeholder_image = placeholder_image.filter(ImageFilter.GaussianBlur(placeholder_blur))
    main_image_out = BytesIO()
    placeholder_out = BytesIO()
    image.save(main_image_out, image_format, quality=90, optimize=True)
    placeholder_image.save(placeholder_out, image_format, quality=placeholder_quality, optimize=True)
    image_size = sys.getsizeof(main_image_out)
    placeholder_size = sys.getsizeof(placeholder_out)
    return ((main_image_out, image_name, content_type, image_size), (placeholder_out, image_name, content_type, placeholder_size))
    




@receiver(pre_save, sender=Post, dispatch_uid="post.generate_placeholder")
def get_post_placeholder(instance, sender, **kwargs):
    if instance._state.adding:
        # get_post_placeholder_helper(instance, 10, 240, 15)
        image, placeholder = optimize_images(instance, 10, 240, 15)
        instance.photo = InMemoryUploadedFile(image[0], field_name="photo", name=image[1], content_type=image[2], size=image[3], charset="utf-8")
        instance.placeholder = InMemoryUploadedFile(placeholder[0], field_name="placeholder", name=placeholder[1], content_type=placeholder[2], size=placeholder[3], charset="utf-8")
    else:
        old_obj = sender.objects.get(pk=instance.id)
        if old_obj.placeholder and old_obj.photo.url != instance.photo.url:
            old_obj.placeholder.delete(False)
        get_post_placeholder_helper(instance, 10, 240, 15)


@receiver(pre_delete, sender=Post, dispatch_uid="post.delete_placeholder")
def delete_post_images(instance, sender, **kwargs):
    object = sender.objects.get(pk=instance.id)
    if (not object.photo or object.photo is not None) and (object.placeholder or object.placeholder is not None):
        object.photo.delete(False)
        object.placeholder.delete(False)