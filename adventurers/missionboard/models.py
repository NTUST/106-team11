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
    def generate(self):
        obj = self.create(
            name=fake.text(),
            posted_by=User.objects.get(id=random.randint(1, User.objects.count())),
            posted_on=fake.date_time_between(start_date="-30d", end_date="-15d", tzinfo=tz('Asia/Taipei')),
            status='',
            application_deadline=fake.date_time_between(start_date="-14d", end_date="+7d", tzinfo=tz('Asia/Taipei')),
            description=fake.text(),
            working_deadline=fake.date_time_between(start_date="+15d", end_date="+30d", tzinfo=tz('Asia/Taipei')),
        )

        skill_list = []
        for n in range(1, random.randint(1,3)):
            skill_list.append(Skill.objects.random_pick())
        obj.required_skills.set(skill_list)
        obj.save()
        return obj


class Mission(models.Model):
    name = models.CharField(max_length=100)
    required_skills = models.ManyToManyField(Skill, related_name='required_skills')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_on = models.DateTimeField()
    status = models.CharField(max_length=20)
    application_deadline = models.DateTimeField()
    working_deadline = models.DateTimeField()
    description = models.TextField()
    applied_by = models.ManyToManyField(User, related_name='applied_by')
    objects = MissionManager()

    def __str__(self):
        return self.name
