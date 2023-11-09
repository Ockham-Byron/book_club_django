from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('login', login_view, name='login'),
    path('register', register_view, name='register'),
    path('logout', custom_logout, name='logout'),

    #verify email urls
    path('verify-email/', verify_email, name='verify-email'),
    path('verify-email/done/', verify_email_done, name='verify-email-done'),
    path('verify-email-confirm/<uidb64>/<token>/', verify_email_confirm, name='verify-email-confirm'),
    path('verify-email/complete/', verify_email_complete, name='verify-email-complete'),
    path('verify-email/change-email/', change_email, name='change-email'),

    #profile url
    path('profile/<slug:slug>', profile, name='profile'),
    
] 