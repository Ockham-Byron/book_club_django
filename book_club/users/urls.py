from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home_view, register, custom_login, custom_logout, profile

urlpatterns = [
    path('', home_view, name='home'),
    path('register', register, name='register'),
    path('login', custom_login, name='login'),
    path('logout', custom_logout, name='logout'),
    path('profile/<slug:slug>', profile, name='profile'),
    
] 