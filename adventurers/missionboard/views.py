from django.shortcuts import render
from missionboard.models import Category, Mission

import random
# from collections import namedtuple
# nt_category = namedtuple('Category', 'name, description')



def index(request):
    categories = Category.objects.all()

    for c in categories:
        c.style = 'style%s' % str(random.randrange(1, 6))
        c.img = 'images/pic%s.jpg' % str(random.randrange(1, 6)).zfill(2)

    context = {'category': categories}
    return render(request, 'index.html', context)
