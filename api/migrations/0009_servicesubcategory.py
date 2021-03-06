# Generated by Django 3.1.7 on 2021-02-28 11:16

from django.db import migrations, models

import api.utils


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_employeecategory_icon"),
    ]

    operations = [
        migrations.CreateModel(
            name="ServiceSubcategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=100)),
                (
                    "icon",
                    models.FileField(
                        default="Employee Category/default.svg",
                        upload_to=api.utils.SubcategoryIconLocation,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
