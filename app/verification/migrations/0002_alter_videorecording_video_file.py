# Generated by Django 5.0.1 on 2024-06-16 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videorecording',
            name='video_file',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
    ]