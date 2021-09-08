from django import dispatch
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from .models import Service, ServiceSubcategory
from .utils import generate_placeholder


def signal_save_placeholder_helper(instance, sender, blur, height, quality):
    # Added new Subcategory so generate new placeholder
    if instance._state.adding:
        # get Placeholder detail
        image_file, image_name, file_size, content_type = generate_placeholder(
            instance.icon, blur, height, quality
        )
        instance.placeholder = InMemoryUploadedFile(
            file=image_file,
            field_name="placeholder",
            name=image_name,
            size=file_size,
            content_type=content_type,
            charset="utf-8",
        )

    # Update Subcategory delete old placeholder
    if not instance._state.adding:
        old_obj = sender.objects.get(pk=instance.id)

        # if there is already a placeholder and we are adding new placeholder then delete old placeholder
        if old_obj.placeholder and instance.icon.url != old_obj.icon.url:
            old_obj.placeholder.delete(False)
        image_file, image_name, file_size, content_type = generate_placeholder(
            instance.icon, 4, 200, 50
        )
        instance.placeholder = InMemoryUploadedFile(
            file=image_file,
            field_name="placeholder",
            name=image_name,
            size=file_size,
            content_type=content_type,
            charset="utf-8",
        )


def signal_delete_placeholder_helper(instance, sender):
    obj = sender.objects.get(pk=instance.id)
    # On subcategory delete delete placeholder as well as original image
    if (not obj.icon or obj.icon is not None) and (
        not obj.placeholder or obj.placeholder is not None
    ):
        obj.icon.delete(False)
        obj.placeholder.delete(False)


@receiver(
    pre_save, sender=ServiceSubcategory, dispatch_uid="subcategory.save_placeholder"
)
def save_subcategory__placeholder(sender, instance, **kwargs):
    signal_save_placeholder_helper(instance, sender, 4, 200, 50)


@receiver(pre_save, sender=Service, dispatch_uid="service.save_placeholder")
def save_service_placeholder(sender, instance, **kwargs):
    signal_save_placeholder_helper(instance, sender, 3, 80, 50)


@receiver(pre_delete, sender=Service, dispatch_uid="service.delete_placeholder")
def delete_service_placeholder(sender, instance, **kwargs):
    signal_delete_placeholder_helper(instance, sender)


@receiver(
    pre_delete, sender=ServiceSubcategory, dispatch_uid="subcategory.delete_placeholder"
)
def delete_subcategory_placeholder(sender, instance, **kwargs):
    signal_delete_placeholder_helper(instance, sender)
