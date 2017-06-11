from django.shortcuts import render, redirect
from missionboard.models import Skill, Mission, Skill


def details(request, mission_id):
    mission = Mission.objects.get(id=mission_id)
    context = {
        'user': request.user,
        'mission': mission
    }
    return render(request, 'CaseView.html', context)


def category(request, skill_id):
    category = Skill.objects.get(id=skill_id)
    missions = Mission.objects.filter(required_skills__in=[category])
    context = {
        'user': request.user,
        'category': category,
        'missions': missions,
    }
    return render(request, 'CategoryView.html', context)
