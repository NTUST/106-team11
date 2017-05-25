from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Mission(models.Model):
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(Category, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    description = models.TextField()
    budgets = models.FloatField()
    worker = models.ManyToManyField(User, related_name='worker')

    def __str__(self):
        return self.task_name
