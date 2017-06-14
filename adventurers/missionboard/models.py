from django.db import models
from django.db.models.aggregates import Count
from django.contrib.auth.models import User

from faker import Factory
from pytz import timezone as tz
import random

fake = Factory.create('zh_TW')


class SkillManager(models.Manager):

    def random_pick(self):
        count = self.count()
        random_index = random.randint(0, count - 1)
        return self.all()[random_index]


class Skill(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    objects = SkillManager()

    def __str__(self):
        return self.name


class MissionManager(models.Manager):

    def random_pick(self):
        count = self.count()
        random_index = random.randint(0, count - 1)
        return self.all()[random_index]


class Mission(models.Model):
    name = models.CharField(max_length=100)
    required_skills = models.ManyToManyField(
        Skill, related_name='required_skills')
    required_level = models.IntegerField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_on = models.DateTimeField()
    status = models.CharField(max_length=20)
    application_deadline = models.DateTimeField()
    working_deadline = models.DateTimeField()
    required_worker_num = models.IntegerField()
    description = models.TextField()
    applied_by = models.ManyToManyField(
        User, related_name='applied_by', blank=True, through='MissionApplication')
    objects = MissionManager()

    def __str__(self):
        return self.name


class MissionApplication(models.Model):
    applied_by = models.ForeignKey(User, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "applied_by: {}, Mission: {}".format(self.applied_by.username, self.mission.name)
