from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from message.models import Message, ChatRoom
from message.serializers import MessageSerializer, ChatSerializer


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]


class ChatViewSet(viewsets.ModelViewSet):
    """
    Chat API
    """
    serializer_class = ChatSerializer
    queryset = ChatRoom.objects.all()

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]
