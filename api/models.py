from django.db import models
from django.db.models.base import Model
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from .utils import EmployeeIconLocation, SubcategoryIconLocation, ServiceIconLocation
from django.utils.timesince import timesince

class EmployeeCategory(models.Model):
    name= models.CharField(max_length=100, db_index=True)
    slug = models.CharField(null=True, blank=True, max_length=100, db_index=True)
    icon = models.FileField(upload_to=EmployeeIconLocation, default='Employee Category/default.svg')

    class Meta:
        index_together = ('id', 'slug')

        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ServiceSubcategory(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True, null=True, blank=True)
    icon = models.ImageField(upload_to=SubcategoryIconLocation, default='Service SubCategory Images/default.jpg')
    created = models.DateTimeField(auto_now_add=True, null=True)
    service_specialist = models.ForeignKey(EmployeeCategory, on_delete=models.CASCADE, null=True, related_name='subcategory')


    class Meta:
        ordering = ('-created',)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    icon = models.ImageField(default='Service Images/default-service.jpg', upload_to=ServiceIconLocation)
    subcategory = models.ForeignKey(ServiceSubcategory, on_delete=models.CASCADE, null=True, related_name='services')
    description = models.TextField(max_length=500, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class CategoryReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='reviews', blank=True)
    category = models.ForeignKey(EmployeeCategory, on_delete=models.CASCADE, null=True, blank=True, related_name='category_reviews')
    star = models.IntegerField(default=5, validators=[MaxValueValidator(5), MinValueValidator(0)])
    review = models.TextField(max_length=500, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment By {self.user.number}"

class CouponCode(models.Model):
    code = models.CharField(max_length=100, db_index=True)
    discount = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=False)
    category = models.ManyToManyField(EmployeeCategory, blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL , blank=True)

    class Meta:
        ordering = ('code',)
    def __str__(self):
        return self.code