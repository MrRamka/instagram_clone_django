from celery import shared_task
from channels.db import database_sync_to_async
from django.db.models import Sum
import logging

from instagram_clone_django.celery import app


@app.task
def update_statistics():
    from core.models import Image, Video, Statistics
    from user_profile.models import Profile
    images_amount = Image.objects.count()
    video_amount = Video.objects.count()
    video_views_amount = Video.objects.aggregate(Sum('views'))
    video_views_amount = video_views_amount.get('views__sum')
    image_likes = Image.objects.aggregate(Sum('likes'))
    video_likes = Video.objects.aggregate(Sum('likes'))
    print(image_likes)
    likes_amount = image_likes.get('likes__sum')
    likes_amount += video_likes.get('likes__sum')
    users_amount = Profile.objects.all().count()

    stat = Statistics()
    stat.image_amount = images_amount
    stat.video_amount = video_amount
    stat.video_views_amount = video_views_amount
    stat.user_amount = users_amount
    stat.likes_amount = likes_amount
    stat.save()
    logging.info('Hello')
    print('Hello')


@app.task
def test():
    print('world')
