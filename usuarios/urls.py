from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as user_views

app_name = 'usuarios'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', user_views.logout_view, name='logout'),
]
