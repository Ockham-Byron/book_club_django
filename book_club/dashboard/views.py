from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model

# Create your views here.
def dashboard_view(request):
  user=request.user

  context = {'user': user}

  return render(request, 'dashboard/dashboard.html', context=context)