# Generated by Django 2.2.28 on 2024-03-17 16:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamefolio_app', '0002_auto_20240314_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='datePosted',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 17, 16, 42, 41, 940428)),
        ),
    ]