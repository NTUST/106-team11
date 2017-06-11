from django.shortcuts import render, redirect
from missionboard.models import Skill, Mission
from missionboard.forms import NewMissionForm
from .auth import get_user


def details(request, mission_id):
    mission = Mission.objects.get(id=mission_id)
    context = {
        'user': get_user(request.user),
        'mission': mission
    }
    return render(request, 'CaseView.html', context)


def category(request, skill_id):
    category = Skill.objects.get(id=skill_id)
    missions = Mission.objects.filter(required_skills__in=[category])
    context = {
        'user': get_user(request.user),
        'category': category,
        'missions': missions,
    }    
    return render(request, 'CategoryView.html', context)


def new_mission(request):
    if request.method == 'GET':
        form = NewMissionForm()
        context = {
            'user': get_user(request.user),
            'form': form,
        }
        return render(request, 'NewMissionView.html', context)
    elif request.method == 'POST':
        form = NewMissionForm(request.POST)
        if form.is_valid():
            context = {
                'form': form,
            }
            print("valid: ")
            print(form.cleaned_data)
            return render(request, 'NewMissionView.html', context)
        else:
            context = {
                'form': form,
            }
            print("invalid: ")
            print(form.cleaned_data)
            print(form.errors)
            return render(request, 'NewMissionView.html', context)
    else:
        print('WTF?')
        return redirect('missionboard_index')
