# Generated by Django 5.0.1 on 2024-06-18 04:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskEyeBlink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expected_count', models.IntegerField()),
                ('detected_count', models.IntegerField(blank=True, null=True)),
                ('accuracy', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VerificationTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_video', models.FileField(blank=True, null=True, upload_to='original_videos/')),
                ('processed_video', models.FileField(blank=True, null=True, upload_to='processed_videos/')),
                ('task_type', models.CharField(choices=[('eye_blink', 'Eye Blink')], max_length=20)),
                ('status', models.CharField(blank=True, choices=[('passed', 'Passed'), ('failed', 'Failed')], max_length=20, null=True)),
                ('task_id', models.PositiveIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
