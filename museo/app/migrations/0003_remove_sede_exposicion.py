# Generated by Django 3.1.2 on 2021-06-27 01:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_sede_exposicion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sede',
            name='exposicion',
        ),
    ]
