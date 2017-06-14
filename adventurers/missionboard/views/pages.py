from django.shortcuts import (
    render, redirect, render_to_response, HttpResponseRedirect)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.utils import timezone

from missionboard.forms import NewMissionForm
from missionboard.models import Skill, Mission, RegisterApplication, MissionApplication
from .auth import get_user

import random
import datetime


def index(request):
    skills = Skill.objects.all().order_by('name')

    context = {
        'user': get_user(request.user),
        'skills': skills,
        'styles': ["style{}".format(n) for n in range(1, 6)],
        'images': ['images/pic{}.jpg'.format(str(n).zfill(2)) for n in range(1, 13)],
    }
    return render(request, 'index.html', context)


def aboutus(request):
    context = {'user': get_user(request.user)}
    return render(request, 'aboutus.html', context)


def donate(request):
    context = {'user': get_user(request.user)}
    return render(request, 'donate.html', context)


def details(request, mission_id):
    m = Mission.objects.get(id=mission_id)
    ma = RegisterApplication.objects.filter(mission=m)

    context = {
        'user': get_user(request.user),
        'm': m,
        'ma': ma,
        'now': timezone.now(),
    }

    return render(request, 'CaseView.html', context)


def category(request, skill_id):
    category = Skill.objects.get(id=skill_id)
    missions = Mission.objects.filter(
        required_skills__in=[category], status='application')
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
                required_worker_num=form.cleaned_data['required_worker_num'],
                status='application',
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
            print(123)
            context = {
                'user': request.user,
                'form': form,
            }
            return render(request, 'NewMissionView.html', context)
    else:
        print('WTF?')
        return redirect('missionboard_index')


@login_required
def case_applied(request, mission_id):
    if request.method == 'POST':
        m = Mission.objects.get(id=mission_id)
        ma_qset = MissionApplication.objects.filter(
            applied_by=request.user, mission=m)
        if ma_qset.count() > 0 and m.application_deadline < timenow.now():
            ma_qset.delete()
            request.user.my_profile.missions_wip.remove(m)
            context = {'user': request.user, 'm': m,
                       'msg': '你已放棄此案件！', 'title': '放棄案件'}
        else:
            if request.user.my_profile.level >= m.required_level:
                ma = MissionApplication.objects.create(
                    applied_by=request.user, mission=m)
                request.user.my_profile.missions_wip.add(m)
                context = {'user': request.user, 'm': m,
                           'msg': '你已成功接案！', 'title': '成功接案'}
            else:
                context = {'user': request.user, 'm': m,
                           'msg': '等級不足，接案失敗！', 'title': '接案失敗'}
        return render(request, 'CaseApplied.html', context)
    else:
        raise Http404("你不能這樣硬闖啦...")


@login_required
def mission_wip(request):
    user = get_user(request.user)
    Missions = Mission.objects.filter(applied_by__in=[user], status='in_progress').order_by('posted_on')
    context = {'Missions': Missions, 'user': user}
    return render_to_response('mission_wip.html', context)


def CheckMissionStatus(mission):
    deadline = mission.application_deadline
    now = timezone.now()
    if mission.status == 'application' and now > deadline:
        return True
    return False


@login_required
def ManageCase(request):
    user = get_user(request.user)
    Missions = Mission.objects.filter(posted_by=user).order_by('posted_on')
    for mission in Missions:
        if CheckMissionStatus(mission):
            Mission.objects.filter(id=mission.id).update(status='abandoned')
    context = {'Missions': Missions, 'user': user}
    return render_to_response('ManageCase.html', context)


@login_required
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
