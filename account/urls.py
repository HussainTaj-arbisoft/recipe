from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import edit, signup

app_name = 'account'

urlpatterns = [
    path('login_form/', LoginView.as_view(redirect_authenticated_user=True),
         name='login_form'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', signup, name='signup'),
    path('edit/', edit, name='edit'),
]
