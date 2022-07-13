# Generated by Django 4.0.5 on 2022-07-11 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='addr',
            field=models.CharField(max_length=256, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='address',
            name='is_default',
            field=models.BooleanField(default=False, verbose_name='is_default'),
        ),
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=models.CharField(max_length=11, verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='address',
            name='receiver',
            field=models.CharField(max_length=20, verbose_name='receiver'),
        ),
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='address',
            name='zip_code',
            field=models.CharField(max_length=6, null=True, verbose_name='zip-code'),
        ),
    ]
