from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    bio = models.CharField(max_length=200, blank=True)
    vk_page = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.username
