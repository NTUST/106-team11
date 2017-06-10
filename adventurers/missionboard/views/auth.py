from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from missionboard.forms import RegisterForm, SigninForm


def signin(request):
    if request.user.is_authenticated:
        return redirect('missionboard_index')

    if request.method == 'GET':
        form = SigninForm()
        context = {'form': form}
        return render(request, 'signin.html', context)
    elif request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            password = form.cleaned_data['password']
            u = authenticate(request, username=username, password=password)
            login(request, u)
            return redirect('missionboard_index')
        else:
            return render(request, 'signin.html', {'form': form})


@login_required
def signout(request):
    logout(request)
    return redirect('missionboard_index')


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            User.objects.create_user(username, email, password)
            return redirect('signin.html')
        else:
            return render(request, 'register.html', {'form': form})
