# Generated by Django 3.1.7 on 2021-03-26 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_order_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='service',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]