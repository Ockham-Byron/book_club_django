from django.urls import path
from .views import home_view, auth_view, custom_logout, profile

urlpatterns = [
    path('', home_view, name='home'),
    path('authentication', auth_view, name='authentication'),
    path('logout', custom_logout, name='logout'),
    path('profile/<slug:slug>', profile, name='profile'),
    
] 