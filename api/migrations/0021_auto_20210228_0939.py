# Generated by Django 3.1.7 on 2021-02-28 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0020_servicesubcategory_icon"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="employeecategory",
            options={"ordering": ("-name",)},
        ),
    ]
