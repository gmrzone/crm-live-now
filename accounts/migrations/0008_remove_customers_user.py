# Generated by Django 3.1 on 2020-09-08 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200908_0057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customers',
            name='user',
        ),
    ]
