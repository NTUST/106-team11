from django.conf.urls import url
from .views import auth, pages

urlpatterns = [
    url(r'^signin', auth.signin, name='missionboard_signin'),
    url(r'^signout', auth.signout, name='missionboard_signout'),
    url(r'^register', auth.register, name='missionboard_register'),
    url(r'^aboutus', pages.aboutus, name='missionboard_aboutus'),
    url(r'^donate', pages.donate, name='missionboard_donate'),
    url(r'^case', pages.case, name='missionboard_case'),
    url(r'^$', pages.index, name='missionboard_index'),
]
