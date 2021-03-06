# Generated by Django 3.1.7 on 2021-05-29 08:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0003_post_category"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="postimage",
            name="post",
        ),
        migrations.AddField(
            model_name="postimage",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
