from django.urls import path
from .views import home_view, register

urlpatterns = [
    path('', home_view, name='home'),
    path('register', register, name='register'),
    
] 