# Generated by Django 3.1.7 on 2021-03-08 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0029_auto_20210307_1205"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="servicesubcategory",
            options={"ordering": ("-created",)},
        ),
    ]
