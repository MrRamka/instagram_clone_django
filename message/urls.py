from django.urls import path, include
from rest_framework.routers import DefaultRouter

from message.api import MessageViewSet, ChatViewSet
from message.views import RoomView, RoomListView, CreateChatRoom

app_name = 'messages'

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'chatroom', ChatViewSet, basename='chatroom')

urlpatterns = [
    path('chats/', RoomListView.as_view(), name='chats'),
    path('<int:id>/', RoomView.as_view(), name='room'),
    path('api/', include(router.urls)),
    path('write/<username>/', CreateChatRoom.as_view(), name='write_to')
]
