# Generated by Django 4.0.1 on 2022-03-31 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0012_profile_auth_code_profile_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='password_reset_code',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]