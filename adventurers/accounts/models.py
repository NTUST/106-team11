from django.db import models
# Create your models here.
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile # or UserenaLanguageBaseProfile

from missionboard.models import Mission, Skill


class Member(UserenaBaseProfile):
# 如果要讓使用者可以選擇語言, 則繼承自UserenaLanguageBaseProfile
    user = models.OneToOneField(User,unique=True,
    verbose_name=_('user'),related_name='my_profile')
    level = models.IntegerField()
    skills = models.ManyToManyField(Skill)
    partners = models.ManyToManyField(User)
    missions_completed = models.ManyToManyField(Mission, related_name='missions_completed')
    missions_wip = models.ManyToManyField(Mission, related_name='missions_wip')
    missions_failed = models.ManyToManyField(Mission, related_name='missions_failed')
    bios = models.TextField()
    contact = models.TextField()

    def __str__(self):
        return self.user.username
