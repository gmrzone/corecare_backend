# Generated by Django 3.1.7 on 2021-03-07 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_categoryreview_category'),
        ('account', '0006_auto_20210305_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='employee_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='api.employeecategory'),
        ),
    ]
