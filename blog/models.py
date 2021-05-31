from django.db import models
from django.conf import settings
from django.utils.text import slugify
from .utils import blog_image_location, blog_images
from api.models import EmployeeCategory
# Create your models here.

class DateFieldAbstract(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Post(DateFieldAbstract):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(EmployeeCategory, on_delete=models.SET_NULL, related_name="category_posts", null=True)
    title = models.CharField(max_length=400, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True, blank=True)
    photo = models.ImageField(upload_to=blog_image_location, default="default_blog.jpg")
    body = models.TextField(max_length=200000)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    class Meta:
        index_together = ('id', "slug")
        ordering = ('-created',)


class PostImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name="images")
    upload = models.ImageField(upload_to=blog_images)

class Comment(DateFieldAbstract):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies")
    comment = models.TextField(max_length=400)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)
    
    
