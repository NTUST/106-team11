from django.conf.urls import url
from .views import auth, pages, eason

urlpatterns = [
    url(r'^signin', auth.signin, name='missionboard_signin'),
    url(r'^signout', auth.signout, name='missionboard_signout'),
    url(r'^register', auth.register, name='missionboard_register'),
    url(r'^aboutus', pages.aboutus, name='missionboard_aboutus'),
    url(r'^donate', pages.donate, name='missionboard_donate'),
    url(r'^new_mission/', eason.new_mission, name='missionboard_new_mission'),
    url(r'^details/(?P<mission_id>\d+)', eason.details, name='missionboard_details'),
    url(r'^category/(?P<skill_id>\d+)', eason.category, name='missionboard_category'),
    url(r'^$', pages.index, name='missionboard_index'),
]
