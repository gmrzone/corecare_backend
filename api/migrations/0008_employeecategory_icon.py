# Generated by Django 3.1.7 on 2021-02-25 18:33

import api.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_employeecategory_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeecategory',
            name='icon',
            field=models.FileField(default='Employee Category/default.svg', upload_to=api.utils.EmployeeIconLocation),
        ),
    ]
