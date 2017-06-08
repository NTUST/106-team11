from django.db import models
# Create your models here.
from django.contrib.auth.models import User  
from django.utils.translation import ugettext as _  
from userena.models import UserenaBaseProfile # or UserenaLanguageBaseProfile
  
class MyProfile(UserenaBaseProfile):
# 如果要讓使用者可以選擇語言, 則繼承自UserenaLanguageBaseProfile
    user = models.OneToOneField(User,unique=True,  
    verbose_name=_('user'),related_name='my_profile')  
