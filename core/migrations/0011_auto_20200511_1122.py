# Generated by Django 3.0.4 on 2020-05-11 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_statistics_likes_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statistics',
            old_name='likes_amount',
            new_name='like_amount',
        ),
        migrations.RenameField(
            model_name='statistics',
            old_name='video_views_amount',
            new_name='video_view_amount',
        ),
    ]