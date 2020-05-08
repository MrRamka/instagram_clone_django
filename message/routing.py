from django.urls import re_path

from . import consumers

# \w stands for "word character", usually [A-Za-z0-9_]. Notice the inclusion of the underscore and digits
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\w+)/$', consumers.ChatConsumer),
]
