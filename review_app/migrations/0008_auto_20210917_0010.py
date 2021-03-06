# Generated by Django 3.2.7 on 2021-09-16 21:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('review_app', '0007_alter_profile_projects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='projects',
        ),
        migrations.AlterField(
            model_name='projects',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myprojects', to=settings.AUTH_USER_MODEL),
        ),
    ]
