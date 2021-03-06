# Generated by Django 3.2.5 on 2021-08-02 16:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0045_auto_20210628_1058"),
    ]

    operations = [
        migrations.AlterField(
            model_name="categoryreview",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="category_reviews",
                to="api.employeecategory",
            ),
        ),
    ]
