from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from user_profile.views import RegistrationView, LoginView, ResetPasswordRequestView, ResetPasswordView, MessageSentView

app_name = 'user_profile'
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('user_profile:login')), name='logout'),
    path('reset/', ResetPasswordRequestView.as_view(), name='reset_request'),
    path('reset-password/<username>/<token>', ResetPasswordView.as_view(), name='reset'),
    path('reset-message/', MessageSentView.as_view(), name='reset_redirect_message'),
]
