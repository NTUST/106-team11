from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='missionboard_index'),
    url(r'^aboutus', views.aboutus, name='missionboard_aboutus'),
]
