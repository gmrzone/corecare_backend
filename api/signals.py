from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from .models import ServiceSubcategory
from .utils import generate_placeholder
from django.core.files.uploadedfile import InMemoryUploadedFile


@receiver(pre_save, sender=ServiceSubcategory, dispatch_uid="subcategory.save_placeholder")
def save_placeholder(sender, instance, **kwargs):
    # Added new Subcategory so generate new placeholder
    if instance._state.adding:
        # get Placeholder detail
        image_file, image_name, file_size, content_type = generate_placeholder(instance.icon, 200)
        instance.placeholder = InMemoryUploadedFile(file=image_file, field_name="placeholder", name=image_name, size=file_size, content_type=content_type, charset='utf-8')

    # Update Subcategory delete old placeholder
    if not instance._state.adding:
        old_obj = sender.objects.get(pk=instance.id)
        
        # if there is already a placeholder and we are adding new placeholder then delete old placeholder
        if (old_obj.placeholder and instance.icon.url != old_obj.icon.url):
            old_obj.placeholder.delete(False)
        image_file, image_name, file_size, content_type = generate_placeholder(instance.icon, 200)
        instance.placeholder = InMemoryUploadedFile(file=image_file, field_name="placeholder", name=image_name, size=file_size, content_type=content_type, charset='utf-8')


@receiver(pre_delete, sender=ServiceSubcategory, dispatch_uid="subcategory.delete_placeholder")
def delete_placeholder(sender, instance, **kwargs):
    image = sender.objects.get(pk=instance.id)
    # On subcategory delete delete placeholder as well as original image
    if (not image.icon or image.icon is not None) and (not image.placeholder or image.placeholder is not None):
        image.icon.delete(False)
        image.placeholder.delete(False)


        
