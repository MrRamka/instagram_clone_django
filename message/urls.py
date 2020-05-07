from django.urls import path

from message import views
from message.views import RoomView

app_name = 'messages'
urlpatterns = [
    # path('<str:room_name>/', views.room, name='room'),
    path('<int:id>/', RoomView.as_view(), name='room'),
]
