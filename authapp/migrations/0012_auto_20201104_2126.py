# Generated by Django 3.1.2 on 2020-11-04 18:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0011_auto_20201104_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 18, 26, 48, 206020, tzinfo=utc)),
        ),
    ]
