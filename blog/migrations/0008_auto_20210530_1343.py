# Generated by Django 3.1.7 on 2021-05-30 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0007_auto_20210530_1232"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="body",
            field=models.TextField(max_length=200000),
        ),
    ]
