# Generated by Django 3.1.7 on 2021-04-06 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0036_auto_20210321_0202"),
    ]

    operations = [
        migrations.AddField(
            model_name="employeecategory",
            name="hiring",
            field=models.BooleanField(default=True),
        ),
    ]
