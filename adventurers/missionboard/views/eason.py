from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

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


@login_required
def new_mission(request):
    if request.method == 'GET':
        form = NewMissionForm()
        context = {
            'user': request.user,
            'form': form,
        }
        return render(request, 'NewMissionView.html', context)
    elif request.method == 'POST':
        form = NewMissionForm(request.POST)
        if form.is_valid():
            m = Mission.objects.create(
                name=form.cleaned_data['name'],
                required_level=form.cleaned_data['required_level'],
                posted_by=request.user,
                posted_on=timezone.now(),
                application_deadline=form.cleaned_data['application_deadline'],
                working_deadline=form.cleaned_data['working_deadline'],
                description=form.cleaned_data['description'],
            )
            m.required_skills.set(form.cleaned_data['required_skills'])
            m.save()

            context = {'user': request.user}
            return redirect('missionboard_details', m.id)
        else:
            context = {
                'user': request.user,
                'form': form,
            }
            return render(request, 'NewMissionView.html', context)
    else:
        print('WTF?')
        return redirect('missionboard_index')
