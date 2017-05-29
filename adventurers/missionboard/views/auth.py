from django.shortcuts import render
from missionboard.forms import RegisterForm, SigninForm

import random
# from collections import namedtuple
# nt_category = namedtuple('Category', 'name, description')


def signin(request):
    if request.method == 'GET':
        form = SigninForm()
        context = {'form': form}
        return render(request, 'signin.html', context)
    elif request.method == 'POST':
        return render(request, 'signin.html')


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        context = {'form': form}

        return render(request, 'register.html', context)

    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            return render(request, 'register.html')
        else:
            return render(request, 'register.html', {'form': form})
