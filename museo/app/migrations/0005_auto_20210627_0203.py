# Generated by Django 3.1.2 on 2021-06-27 02:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_exposicion_sede'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exposicion',
            name='sede',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expos', to='app.sede'),
        ),
    ]