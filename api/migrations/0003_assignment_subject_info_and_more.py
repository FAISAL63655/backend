# Generated by Django 4.2.7 on 2025-04-14 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_note_subject_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='subject_info',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='اسم المادة'),
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='subject_info',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='اسم المادة'),
        ),
    ]
