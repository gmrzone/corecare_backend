# Generated by Django 3.1.7 on 2021-02-25 18:25

from django.db import migrations, models

import api.utils


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_auto_20210225_0907"),
    ]

    operations = [
        migrations.AddField(
            model_name="employeecategory",
            name="icon",
            field=models.FileField(
                default="Employee Category/defauly.svg",
                upload_to=api.utils.EmployeeIconLocation,
            ),
        ),
    ]
