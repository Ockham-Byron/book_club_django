from django.urls import path
from .views import *



urlpatterns = [
  path('add-group/', add_group_view, name="add-group"),
  
]