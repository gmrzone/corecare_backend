# Generated by Django 3.1.7 on 2021-03-05 15:11

import account.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210305_0657'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='photo',
            field=models.ImageField(default='default-profile.png', upload_to=account.utils.profile_pic_loc),
        ),
    ]
