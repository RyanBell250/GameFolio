# Generated by Django 2.2.28 on 2024-03-22 09:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamefolio_app', '0003_auto_20240322_0541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='datePosted',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 22, 9, 0, 7, 279865)),
        ),
    ]