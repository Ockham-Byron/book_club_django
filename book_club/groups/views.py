from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from .forms import *


@login_required
def add_group_view(request):
    form = AddGroupForm()
    
    user= request.user
    if request.method == 'POST':
        form = AddGroupForm(request.POST, request.FILES)
        group_pic = request.FILES.get('group_pic')
        
        if form.is_valid():
            form.instance.leader = user
            group = form.save()
            group.group_pic = group_pic
            group.members.add(user)
            group.save()
            group_name = group.name
            messages.success(request, _(f'New group {group_name} created successfully'), extra_tags=_('Great !'))
            return redirect('all_circles')

    return render(request, 'groups/add_group.html', {'form': form,})

