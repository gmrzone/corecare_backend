# Generated by Django 3.1.7 on 2021-02-28 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0018_auto_20210228_0604"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="servicesubcategory",
            name="icon",
        ),
    ]
