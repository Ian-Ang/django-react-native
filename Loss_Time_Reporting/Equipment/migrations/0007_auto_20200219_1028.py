# Generated by Django 2.2 on 2020-02-19 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Equipment', '0006_auto_20200218_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='spesifikasi',
            name='s1',
            field=models.CharField(max_length=100, null=True, verbose_name='Spesifikasi 1'),
        ),
        migrations.AddField(
            model_name='spesifikasi',
            name='vs1',
            field=models.CharField(max_length=100, null=True, verbose_name='Value 1'),
        ),
    ]
