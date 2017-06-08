from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Skill(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Mission(models.Model):
    name = models.CharField(max_length=100)
    required_skills = models.ManyToManyField(Skill, related_name='required_skills')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_on = models.DateTimeField()
    status = models.CharField(max_length=20)
    application_deadline = models.DateTimeField()
    description = models.TextField()
    applied_by = models.ManyToManyField(User, related_name='applied_by')

    def __str__(self):
        return self.name
