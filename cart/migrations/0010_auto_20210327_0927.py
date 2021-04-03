# Generated by Django 3.1.7 on 2021-03-27 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_order_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='razor_pay_id',
            new_name='razorpay_order_id',
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay_signature',
            field=models.CharField(blank=True, db_index=True, max_length=300, null=True),
        ),
    ]