from django.shortcuts import render, redirect, render_to_response, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from missionboard.models import Skill, Mission, RegisterApplication, MissionApplication
from django.contrib.auth.models import User
from missionboard.forms import NewMissionForm
from .auth import get_user


def CheckMissionStatus(mission):
    deadline = mission.application_deadline
    now = timezone.now()
    if mission.status == 'application' and now > deadline:
        return True
    return False


def ManageCase(request):
    user = get_user(request.user)
    Missions = Mission.objects.filter(posted_by=user).order_by('posted_on')
    for mission in Missions:
        if CheckMissionStatus(mission):
            Mission.objects.filter(id=mission.id).update(status='abandoned')
    context = {'Missions': Missions, 'user': user}
    return render_to_response('ManageCase.html', context)


def Managedetails(request, mission_id):
    mission = Mission.objects.get(id=mission_id)
    if request.method == 'POST':
        if CheckMissionStatus(mission):
            Mission.objects.filter(id=mission.id).update(status='abandoned')
            return render(request, 'ManageCaseView.html', context)
        elif request.POST.get('worker_hidden') != None and mission.status == 'application':
            userstr = request.POST.get('worker_hidden')
            userlist = userstr.split(',')
            for i in userlist:
                new_user = User.objects.filter(username=i).all()
                User.objects.filter(username=i)[
                    0].my_profile.missions_wip.add(mission)
                MissionApplication.objects.create(
                    applied_by=new_user[0], mission=mission)
            Mission.objects.filter(id=mission.id).update(status='in_progress')
        elif 'success_hidden' in request.POST and mission.status == 'in_progress':
            userstr = request.POST.get('success_hidden')
            userlist = userstr.split(',')[:-1]
            for i in userlist:
                User.objects.filter(username=i)[
                    0].my_profile.missions_completed.add(mission)
                User.objects.filter(username=i)[
                    0].my_profile.missions_wip.remove(mission)
            Mission.objects.filter(id=mission.id).update(status='completed')
        elif 'fail_hidden' in request.POST and mission.status == 'in_progress':
            userstr = request.POST.get('success_hidden')
            userlist = userstr.split(',')[:-1]
            for i in userlist:
                User.objects.filter(username=i)[
                    0].my_profile.missions_failed.add(mission)
                User.objects.filter(username=i)[
                    0].my_profile.missions_wip.remove(mission)
            Mission.objects.filter(id=mission.id).update(status='failed')
        return HttpResponseRedirect(mission_id)
    worker_list = RegisterApplication.objects.filter(mission=mission)
    context = {
        'user': get_user(request.user),
        'mission': mission,
        'worker': worker_list,
    }
    return render(request, 'ManageCaseView.html', context)
