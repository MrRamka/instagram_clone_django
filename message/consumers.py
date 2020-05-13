import json

from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from message.models import Message, ChatRoom
from user_profile.models import Profile


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        print(dir(self))
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        user = await database_sync_to_async(Profile.objects.get)(username=username)
        chat = await database_sync_to_async(ChatRoom.objects.get)(id=self.room_name)
        message_obj = await database_sync_to_async(Message.objects.create)(chat=chat,
                                                                           text=message,
                                                                           author=user)
        time = message_obj.time.strftime('%I:%M %p')
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'time': time
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        time = event['time']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'time': time
        }))
