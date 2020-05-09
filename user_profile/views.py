from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from user_profile.forms import RegistrationForm, LoginForm


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'user_profile/register.html'
    success_url = reverse_lazy('user_profile:login')


class LoginView(LoginView):
    template_name = 'user_profile/login.html'
    success_url = reverse_lazy('core:feed')

    # form_class = LoginForm
