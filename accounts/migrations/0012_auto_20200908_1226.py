# Generated by Django 3.1 on 2020-09-08 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20200908_0714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='profile_pic',
            field=models.ImageField(blank=True, default='images/default_profile.png', null=True, upload_to=''),
        ),
    ]