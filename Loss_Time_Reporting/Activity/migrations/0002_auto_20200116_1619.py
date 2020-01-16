# Generated by Django 2.2 on 2020-01-16 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Activity', '0001_initial'),
        ('Equipment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='status_created_by_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='status',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='status_updated_by_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity_created_by_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='equipment_ids',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Equipment.Equipment'),
        ),
        migrations.AddField(
            model_name='activity',
            name='status_ids',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Activity.Status'),
        ),
        migrations.AddField(
            model_name='activity',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity_update_by_user', to=settings.AUTH_USER_MODEL),
        ),
    ]