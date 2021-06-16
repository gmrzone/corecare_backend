from api.utils import generate_placeholder
from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save
from .models import Post
from django.core.files.uploadedfile import InMemoryUploadedFile


def get_post_placeholder_helper(instance, blur, height, quality):
    image_file, image_name, file_size, content_type = generate_placeholder(instance.photo, blur, height, quality)
    instance.placeholder = InMemoryUploadedFile(image_file, field_name="placeholder", name=image_name, size=file_size, content_type=content_type, charset="utf-8")

@receiver(pre_save, sender=Post, dispatch_uid="post.generate_placeholder")
def get_post_placeholder(instance, sender, **kwargs):
    if instance._state.adding:
        get_post_placeholder_helper(instance, 10, 240, 15)
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