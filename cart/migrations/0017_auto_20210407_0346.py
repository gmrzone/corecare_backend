# Generated by Django 3.1.7 on 2021-04-07 10:46

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0016_order_complete_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="complete_by",
            field=models.DateTimeField(
                default=datetime.datetime(2021, 4, 10, 10, 46, 28, 430341, tzinfo=utc)
            ),
        ),
    ]
