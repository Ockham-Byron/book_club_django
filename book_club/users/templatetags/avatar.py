from django import template
from django.template.loader import render_to_string

import hashlib

register = template.Library()

NUM_COLORS = 8


@register.filter
def avatar(user):
    letter = user.username[0].upper() if user.username else '?'
    color_ix = int(hashlib.md5(str(user.id).encode()).hexdigest(), 16) % NUM_COLORS
    context = {'color_ix': color_ix, 'letter': letter}
    return render_to_string('users/avatar.svg', context)
