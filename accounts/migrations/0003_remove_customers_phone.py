# Generated by Django 3.1 on 2020-09-03 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_order_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customers',
            name='phone',
        ),
    ]
