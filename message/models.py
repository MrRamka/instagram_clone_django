from django.db import models

# Create your models here.
from user_profile.models import Profile


class ChatRoom(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, 'Dialog'),
        (CHAT, 'Chat')
    )

    type = models.CharField(
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(Profile)

    def __str__(self):
        return f'Type: {self.type} Members: {self.members}'


class Message(models.Model):
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    is_readed = models.BooleanField(default=False)

    class Meta:
        ordering = ['time']

    def __str__(self):
        return f'{self.author} - {self.text} ({self.time})'
