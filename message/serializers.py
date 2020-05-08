from rest_framework import serializers

from message.models import Message, ChatRoom


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    # messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = '__all__'
