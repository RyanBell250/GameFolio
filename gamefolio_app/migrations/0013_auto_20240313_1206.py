# Generated by Django 2.2.28 on 2024-03-13 12:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamefolio_app', '0012_merge_20240313_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='datePosted',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 13, 12, 6, 4, 211390)),
        ),
    ]