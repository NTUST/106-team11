from django.conf.urls import url
from .views import auth, pages

urlpatterns = [
    url(r'^signin', auth.signin, name='missionboard_signin'),
    url(r'^signout', auth.signout, name='missionboard_signout'),
    url(r'^register', auth.register, name='missionboard_register'),
    url(r'^aboutus', pages.aboutus, name='missionboard_aboutus'),
    url(r'^donate', pages.donate, name='missionboard_donate'),
    url(r'^mission_wip/', pages.mission_wip, name='missionboard_mission_wip'),
    url(r'^managecase/(?P<mission_id>\d+)', pages.Managedetails, name='missionboard_manage_details'),
    url(r'^managecase/', pages.ManageCase, name='missionboard_manage_case'),
    url(r'^new_mission/', pages.new_mission, name='missionboard_new_mission'),
    url(r'^case_applied/(?P<mission_id>\d+)', pages.case_applied, name='missionboard_case_applied'),
    url(r'^details/(?P<mission_id>\d+)', pages.details, name='missionboard_details'),
    url(r'^category/(?P<skill_id>\d+)', pages.category, name='missionboard_category'),
    url(r'^$', pages.index, name='missionboard_index'),
]
