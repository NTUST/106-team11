from django.conf.urls import url, include
from django.contrib import admin
from userena import views as userena_views
from accounts.forms import SignupFormExtra
from . import views as project_views

urlpatterns = [
    url(r'^missionboard/', include('missionboard.urls')),
    url(r'^accounts/signup/$',userena_views.signup,{'signup_form': SignupFormExtra}),
    url(r'^accounts/', include('userena.urls')),
    url(r'^admin/', admin.site.urls),    
    url(r'^$', project_views.index),
]
