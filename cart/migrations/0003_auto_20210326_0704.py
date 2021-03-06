# Generated by Django 3.1.7 on 2021-03-26 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0036_auto_20210321_0202"),
        ("cart", "0002_auto_20210326_0658"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="related_orders",
                to="api.employeecategory",
            ),
        ),
    ]
