# Generated by Django 3.1.7 on 2021-03-06 05:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0027_categoryreview_category"),
        ("account", "0005_customuser_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="employee_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="user",
                to="api.employeecategory",
            ),
        ),
    ]
