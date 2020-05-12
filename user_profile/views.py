from smtplib import SMTP

from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, TemplateView

from core.tasks import send_email_task
from instagram_clone_django import settings
from user_profile.forms import RegistrationForm, LoginForm, PasswordResetRequestForm, PasswordResetForm
from user_profile.models import Profile, UserToken


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'user_profile/register.html'
    success_url = reverse_lazy('user_profile:login')


class LoginView(LoginView):
    template_name = 'user_profile/login.html'
    success_url = reverse_lazy('core:feed')

    # form_class = LoginForm


class ResetPasswordRequestView(FormView):
    template_name = 'user_profile/reset.html'
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy('user_profile:reset_redirect_message')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email"]

            # find user
            user = Profile.objects.get(email=data)
            token_raw = default_token_generator.make_token(user)
            UserToken.objects.create(user=user, token=token_raw)
            reset_password_link = str('http://localhost:8000') + reverse('user_profile:reset',
                                                                         kwargs={
                                                                             'username': user.username,
                                                                             'token': token_raw
                                                                         }
                                                                         )

            send_email_task.delay(
                subject='Reset password',
                to_email=user.email,
                from_email=settings.EMAIL_HOST_USER,
                template='user_profile/reset_message.html',
                args={'url': reset_password_link}
            )
        return self.form_valid(form)


class UserResetPasswordAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        username = kwargs['username']
        user = Profile.objects.get(username=username)
        token = kwargs['token']
        try:
            UserToken.objects.get(user=user, token=token)
        except UserToken.DoesNotExist:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class ResetPasswordView(UserResetPasswordAccessMixin, FormView):
    form_class = PasswordResetForm
    template_name = 'user_profile/reset_conf.html'
    success_url = reverse_lazy('user_profile:login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["password"]
            username = kwargs['username']
            token = kwargs['token']
            user_token = UserToken.objects.get(user__username=username, token=token)

            user = user_token.user
            user.set_password(data)
            user.save()

            user_token.delete()

        return self.form_valid(form)


class MessageSentView(TemplateView):
    template_name = 'user_profile/message_sent.html'
