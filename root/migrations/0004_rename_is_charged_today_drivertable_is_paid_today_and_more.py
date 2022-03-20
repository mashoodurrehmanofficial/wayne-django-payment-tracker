# Generated by Django 4.0.1 on 2022-03-20 02:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0003_alter_drivertable_last_charged_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='drivertable',
            old_name='is_charged_today',
            new_name='is_paid_today',
        ),
        migrations.RenameField(
            model_name='drivertable',
            old_name='last_charged_date',
            new_name='last_paid_date',
        ),
        migrations.AddField(
            model_name='drivertable',
            name='is_rent_deducted_today',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='drivertable',
            name='last_rent_deduction_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]