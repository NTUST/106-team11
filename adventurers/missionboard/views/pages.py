from django.shortcuts import render
from missionboard.models import Mission, Skill

import random
# from collections import namedtuple
# nt_category = namedtuple('Category', 'name, description')


def index(request):
    skills = Skill.objects.all()

    for c in skills:
        c.style = 'style%s' % str(random.randrange(1, 6))
        c.img = 'images/pic%s.jpg' % str(random.randrange(1, 13)).zfill(2)

    if request.user.is_authenticated:
        context = {'u':request.user, 'skills': skills}
    else:
        context = {'skills': skills}
    return render(request, 'index.html', context)

def aboutus(request):
    return render(request, 'aboutus.html')

def donate(request):
    return render(request, 'donate.html')
