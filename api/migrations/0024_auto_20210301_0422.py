# Generated by Django 3.1.7 on 2021-03-01 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20210228_0941'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='employeecategory',
            index_together={('id', 'slug')},
        ),
    ]