from django.shortcuts import render, redirect,render_to_response
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from missionboard.models import Skill, Mission
from missionboard.forms import NewMissionForm
from .auth import get_user

def ManageCase(request):
    user = get_user(request.user)
    Missions = Mission.objects.filter(posted_by=user).order_by('posted_on')

    context={'Missions':Missions}
    return render_to_response('ManageCase.html',context)

def Managedetails(request, mission_id):
    mission = Mission.objects.get(id=mission_id)
    context = {
        'user': get_user(request.user),
        'mission': mission
    }
    return render(request, 'ManageCaseView.html', context)
