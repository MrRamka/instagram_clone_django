from django.contrib import admin

from message.models import Message, ChatRoom


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    pass
