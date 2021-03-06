# Generated by Django 2.2 on 2020-01-29 06:42

import Activity.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0002_auto_20200116_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='no',
            field=models.IntegerField(default=Activity.models.Activity.ids, editable=False, unique=True, verbose_name='Code'),
        ),
        migrations.AddField(
            model_name='status',
            name='no',
            field=models.IntegerField(default=Activity.models.Status.ids, editable=False, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='id',
            field=models.CharField(editable=False, max_length=14, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='id',
            field=models.CharField(editable=False, max_length=30, primary_key=True, serialize=False, unique=True),
        ),
    ]
