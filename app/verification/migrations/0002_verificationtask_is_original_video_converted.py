# Generated by Django 5.0.1 on 2024-06-18 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationtask',
            name='is_original_video_converted',
            field=models.BooleanField(default=False),
        ),
    ]
