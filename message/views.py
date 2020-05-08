from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, RedirectView

from message.models import ChatRoom, Message
from user_profile.models import Profile


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


class RoomListView(ListView, LoginRequiredMixin):
    template_name = 'message/chat_list.html'
    model = ChatRoom

    def get_queryset(self):
        queryset = ChatRoom.objects.filter(members__username=self.request.user.username)
        return queryset


class CreateChatRoom(TemplateView, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        target_user = Profile.objects.get(username=kwargs['username'])

        # Chats with current user and target user
        chats = ChatRoom.objects.filter(members__username__in=[request.user]).filter(
            members__username__in=[target_user]).filter(type=ChatRoom.DIALOG)

        chat_d = chats.first()
        if not chat_d:
            chat_d = ChatRoom.objects.create()
            chat_d.type = ChatRoom.DIALOG
            chat_d.members.add(target_user, request.user)
            chat_d.save()

        return HttpResponseRedirect(reverse('messages:room', args=[chat_d.pk]))
