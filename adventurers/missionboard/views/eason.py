from django.shortcuts import render, redirect, get_object_or_404
from missionboard.models import Mission, Skill

def details(request, mission_id):
    mission = get_object_or_404(Mission, pk=mission_id)
    context = {
        'user': request.user,
        'mission': mission
    }
    return render(request, 'CaseView.html', context)
