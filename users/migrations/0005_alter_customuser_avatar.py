# Generated by Django 3.2.10 on 2021-12-20 10:59

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0004_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars'),
        ),
    ]
