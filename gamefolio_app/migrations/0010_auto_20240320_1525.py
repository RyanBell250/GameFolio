# Generated by Django 2.2.28 on 2024-03-20 15:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamefolio_app', '0009_auto_20240320_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='datePosted',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 15, 25, 1, 268223)),
        ),
    ]
