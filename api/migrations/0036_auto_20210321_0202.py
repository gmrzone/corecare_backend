# Generated by Django 3.1.7 on 2021-03-21 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0035_contact"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="email",
            field=models.EmailField(db_index=True, max_length=100),
        ),
    ]
