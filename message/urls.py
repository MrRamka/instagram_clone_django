from django.urls import path

from message.views import RoomView, RoomListView, CreateChatRoom

app_name = 'messages'
urlpatterns = [
    path('chats/', RoomListView.as_view(), name='chats'),
    path('<int:id>/', RoomView.as_view(), name='room'),
    path('write/<username>/', CreateChatRoom.as_view(), name='write_to')
]
