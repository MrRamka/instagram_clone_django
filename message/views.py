from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from message.models import ChatRoom, Message


def room(request, room_name):
    return render(request, 'message/room.html', {
        'room_name': room_name
    })


class ChatAccessMixin(AccessMixin):
    """Verify that the current user is member of chat."""

    def dispatch(self, request, *args, **kwargs):
        chat = ChatRoom.objects.get(id=request.kwargs['id'])
        if not request.user.is_authenticated and request.user not in chat.members:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class RoomView(TemplateView, ChatAccessMixin):
    template_name = 'message/dialog.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        room_id = self.kwargs['id']
        ctx['room_id'] = room_id

        messages = Message.objects.filter(chat_id=room_id)[:10]
        ctx['messages'] = messages

        chat = ChatRoom.objects.get(id=room_id)
        ctx['chat'] = chat
        return ctx
