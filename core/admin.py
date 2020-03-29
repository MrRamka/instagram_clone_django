from django.contrib import admin

from core.models import (HashTag, Place, Image, Video,
                         ImageComment, VideoComment, ImageLike, VideoLike)


@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    ordering = ['hashtag']
    list_display = ['hashtag']


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    ordering = ['place_name']
    list_display = ['place_name']
    search_fields = ['place_name']
    prepopulated_fields = {'place_slug': ('place_name',)}


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['user', 'image_obj', 'posted_on']
    ordering = ['posted_on']
    search_fields = ['user', 'description', 'place', 'hashtag']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['user', 'video_obj', 'posted_on', 'views']
    ordering = ['posted_on']
    search_fields = ['user', 'description', 'place', 'hashtag']


@admin.register(ImageComment)
class ImageCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'posted_on', 'image', 'comment_body']
    ordering = ['user']
    search_fields = ['user', 'comment_body']


@admin.register(VideoComment)
class VideoCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'posted_on', 'video', 'comment_body']
    ordering = ['user']
    search_fields = ['user', 'comment_body']


@admin.register(ImageLike)
class ImageLikeAdmin(admin.ModelAdmin):
    ordering = ['user']


@admin.register(VideoLike)
class VideoLikeAdmin(admin.ModelAdmin):
    ordering = ['user']
