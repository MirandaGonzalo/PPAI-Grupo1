# Generated by Django 3.1.2 on 2021-06-27 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20210627_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exposicion',
            name='sede',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sede'),
        ),
    ]