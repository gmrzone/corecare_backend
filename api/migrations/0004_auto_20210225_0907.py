# Generated by Django 3.1.7 on 2021-02-25 17:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api", "0003_auto_20210225_0455"),
    ]

    operations = [
        migrations.AlterField(
            model_name="couponcode",
            name="category",
            field=models.ManyToManyField(blank=True, to="api.EmployeeCategory"),
        ),
        migrations.AlterField(
            model_name="couponcode",
            name="users",
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
