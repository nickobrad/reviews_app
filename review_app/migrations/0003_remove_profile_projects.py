# Generated by Django 3.2.7 on 2021-09-16 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review_app', '0002_alter_profile_profile_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='projects',
        ),
    ]
