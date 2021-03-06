# Generated by Django 3.1.7 on 2021-05-31 23:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0013_auto_20210531_2212"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="email",
            field=models.EmailField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="comment",
            name="name",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="comment",
            name="parent",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="replies",
                to="blog.comment",
            ),
        ),
    ]
