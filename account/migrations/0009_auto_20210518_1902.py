# Generated by Django 3.1.7 on 2021-05-18 19:02

import account.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20210403_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='number',
            field=models.CharField(db_index=True, max_length=10, unique=True, validators=[account.validators.number_validator]),
        ),
    ]