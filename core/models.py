from django.db import models

from core.validators import HashTagValidator
from user_profile.models import Profile


class HashTag(models.Model):
    hashtag_validator = HashTagValidator()

    hashtag = models.CharField(max_length=50, validators=[hashtag_validator], unique=True)

    def __str__(self):
        return f'{self.hashtag}'


class Place(models.Model):
    place_name = models.CharField(max_length=50)
    place_slug = models.SlugField(max_length=50)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f'{self.place_name}'

    class Meta:
        unique_together = (('id', 'place_slug'),)
        ordering = ('place_name',)


class InstagramObject(models.Model):
    description = models.CharField(max_length=150, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    hashtag = models.ForeignKey(HashTag, on_delete=models.CASCADE, blank=True, null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        abstract = True


def get_user_image_folder(instance, filename):
    return f'{instance.user.username}/photos/{filename}'


def get_user_video_folder(instance, filename):
    return f'{instance.user.username}/videos/{filename}'


class Image(InstagramObject):
    image_obj = models.ImageField(upload_to=get_user_image_folder)
    likes = models.ManyToManyField(Profile, blank=True, related_name='image_liked_by')

    def __str__(self):
        return f'{self.user} {self.description} {self.posted_on} image'


class Video(InstagramObject):
    video_obj = models.FileField(upload_to=get_user_video_folder)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(Profile, blank=True, related_name='video_liked_by')

    def __str__(self):
        return f'{self.user} {self.description} {self.posted_on} video {self.views}'


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment_body = models.CharField(max_length=250)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} {self.comment_body} {self.posted_on}'

    class Meta:
        abstract = True


class ImageComment(Comment):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


class VideoComment(Comment):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)


# class Like(models.Model):
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#
#     class Meta:
#         abstract = True
#
#
# class ImageLike(Like):
#     image = models.ForeignKey(Image, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.user} to {self.image.user} image: {self.image.image_obj}'
#
#     class Meta:
#         unique_together = (('user', 'image'),)
#
#
# class VideoLike(Like):
#     video = models.ForeignKey(Video, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.user} to {self.video.user} video: {self.video.video_obj}'
#
#     class Meta:
#         unique_together = (('user', 'video'),)
