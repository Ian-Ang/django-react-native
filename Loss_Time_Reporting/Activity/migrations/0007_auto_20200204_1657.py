# Generated by Django 2.2 on 2020-02-04 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0006_auto_20200129_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='start_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='start_time',
            field=models.TimeField(null=True),
        ),
    ]
