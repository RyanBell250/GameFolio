# Generated by Django 2.2.28 on 2024-03-19 19:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamefolio_app', '0004_auto_20240319_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='datePosted',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 19, 19, 58, 19, 294775)),
        ),
    ]
