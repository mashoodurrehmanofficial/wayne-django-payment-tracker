# Generated by Django 4.0.1 on 2022-03-20 02:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0002_alter_drivertable_last_charged_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drivertable',
            name='last_charged_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
