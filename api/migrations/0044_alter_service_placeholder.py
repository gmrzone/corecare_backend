# Generated by Django 3.2.4 on 2021-06-16 13:17

from django.db import migrations, models

import api.utils


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0043_service_placeholder"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="placeholder",
            field=models.ImageField(
                blank=True, null=True, upload_to=api.utils.ServicePlaceholderLocation
            ),
        ),
    ]
