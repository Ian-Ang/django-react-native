# Generated by Django 2.2 on 2020-01-29 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0005_activity_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]