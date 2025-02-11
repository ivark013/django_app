# Generated by Django 5.1.4 on 2025-02-03 00:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camera',
            name='last_active',
        ),
        migrations.AlterField(
            model_name='alert',
            name='camera',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alerts', to='dashboard.camera'),
        ),
        migrations.AlterField(
            model_name='alert',
            name='severity',
            field=models.CharField(choices=[('Low', 'منخفض'), ('Medium', 'متوسط'), ('High', 'عالي')], max_length=50),
        ),
        migrations.AlterField(
            model_name='camera',
            name='camera_id',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='notificationsettings',
            name='telegram_chat_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='notificationsettings',
            name='whatsapp_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
