import smtplib

from celery import shared_task
from channels.db import database_sync_to_async
from django.core.mail import send_mail
from django.db.models import Sum
import logging

from django.template.loader import render_to_string

from instagram_clone_django import settings
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
    likes_amount = image_likes.get('likes__sum')
    likes_amount += video_likes.get('likes__sum')
    users_amount = Profile.objects.all().count()

    stat = Statistics()
    stat.image_amount = images_amount
    stat.video_amount = video_amount
    stat.video_view_amount = video_views_amount
    stat.user_amount = users_amount
    stat.like_amount = likes_amount
    stat.save()


@app.task
def test():
    print('world')


@app.task
def send_email_task(subject, from_email, to_email, template, args):
    """
    Send email
    :param subject:
    :param from_email:
    :param to_email:
    :param template:
    :param args:
    :return:
    """
    server = smtplib.SMTP(settings.EMAIL_HOST + ':' + str(settings.EMAIL_PORT))
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    html = render_to_string(template, args)
    send_mail(
        subject=subject,
        message='',
        from_email=from_email,
        recipient_list=[to_email],
        html_message=html
    )
