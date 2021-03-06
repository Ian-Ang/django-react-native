# Generated by Django 2.2 on 2020-01-16 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Locate',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True, max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('updated_on', models.DateTimeField(blank=True, null=True, verbose_name='Updated on')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locate_created_by_user', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locate_updated_by_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.CharField(editable=False, max_length=7, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50, verbose_name='Equipment')),
                ('qr_code', models.CharField(max_length=12, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True, max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('updated_on', models.DateTimeField(blank=True, null=True, verbose_name='Updated on')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipment_created_by_user', to=settings.AUTH_USER_MODEL)),
                ('locate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Equipment.Locate')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipment_updated_by_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
