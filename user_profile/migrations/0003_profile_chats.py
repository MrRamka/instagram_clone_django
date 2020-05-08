# Generated by Django 3.0.4 on 2020-05-06 15:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_auto_20200329_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='chats',
            field=models.ManyToManyField(blank=True, related_name='_profile_chats_+', to=settings.AUTH_USER_MODEL),
        ),
    ]