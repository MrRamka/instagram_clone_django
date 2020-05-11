from django.contrib import admin
from django.db.models import Count, F
from django.urls import reverse
from django.utils.safestring import mark_safe

from core.models import (HashTag, Place, Image, Video,
                         ImageComment, VideoComment, Statistics)


class HashTagInline(admin.TabularInline):
    model = HashTag


@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    search_fields = ['hashtag']
    ordering = ['hashtag']
    list_display = ['hashtag']


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    ordering = ['place_name']
    list_display = ['place_name', 'longitude', 'latitude']
    search_fields = ['place_name']
    list_editable = ['longitude', 'latitude']
    prepopulated_fields = {'place_slug': ('place_name',)}


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['user', 'image_obj', 'hashtag', 'posted_on', 'place', 'image_likes']
    ordering = ['posted_on']
    search_fields = ['user__username', 'hashtag__hashtag', 'place__place_name']
    list_filter = ['posted_on', 'user', 'place', 'hashtag']

    def image_likes(self, obj):
        return obj.image_likes

    def get_queryset(self, request):
        qs = Image.objects.annotate(image_likes=Count('likes'))
        return qs

    image_likes.admin_order_field = 'image_likes'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['user', 'video_obj', 'posted_on', 'views', 'place', 'hashtag', 'video_likes']
    ordering = ['posted_on', 'views']
    search_fields = ['user', 'description', 'place', 'hashtag']
    list_filter = ['posted_on', 'user', 'place', 'hashtag']
    readonly_fields = ['views']

    def video_likes(self, obj):
        return obj.video_likes

    def get_queryset(self, request):
        qs = Video.objects.annotate(video_likes=Count('likes'))
        return qs

    video_likes.admin_order_field = 'video_likes'


@admin.register(ImageComment)
class ImageCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'posted_on', 'image_url', 'comment_body']
    ordering = ['user', 'posted_on']
    search_fields = ['user__username', 'comment_body']
    list_filter = ['posted_on']

    def image_url(self, obj):
        display_text = ", ".join([
            "<a href={}>{}</a>".format(
                reverse('admin:{}_{}_change'.format(obj._meta.app_label, 'image'),
                        args=(obj.image.id,)),
                obj.image.image_obj)

        ])
        if display_text:
            return mark_safe(display_text)
        return "-"

    image_url.short_description = 'Image'


@admin.register(VideoComment)
class VideoCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'posted_on', 'video_url', 'comment_body']
    # ordering = ['user', 'posted_on']
    search_fields = ['user__username', 'comment_body']
    list_filter = ['posted_on']

    def video_url(self, obj):
        display_text = ", ".join([
            "<a href={}>{}</a>".format(
                reverse('admin:{}_{}_change'.format(obj._meta.app_label, 'video'),
                        args=(obj.video.id,)),
                obj.video.video_obj)

        ])
        if display_text:
            return mark_safe(display_text)
        return "-"

    video_url.short_description = 'Video'


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'image_amount', 'video_amount', 'video_view_amount', 'like_amount', 'user_amount']
