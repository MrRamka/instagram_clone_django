from django.contrib.auth.views import  LogoutView
from django.urls import path, reverse_lazy

from user_profile.views import RegistrationView, LoginView

app_name = 'user_profile'
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('user_profile:login')), name='logout'),
]
