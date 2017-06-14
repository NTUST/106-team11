from django.shortcuts import render, redirect
from missionboard.models import Mission, Skill
from .auth import get_user

import random
# from collections import namedtuple
# nt_category = namedtuple('Category', 'name, description')


def index(request):
    print(Skill.objects.all())
    skills = Skill.objects.all().order_by('name')

    for c in skills:
        c.style = 'style%s' % str(random.randrange(1, 6))
        c.img = 'images/pic%s.jpg' % str(random.randrange(1, 13)).zfill(2)

    context = {'user': get_user(request.user), 'skills': skills}
    return render(request, 'index.html', context)


def aboutus(request):
    context = {'user': get_user(request.user)}
    return render(request, 'aboutus.html', context)


def donate(request):
    context = {'user': get_user(request.user)}
    return render(request, 'donate.html', context)
