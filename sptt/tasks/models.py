from django.contrib.auth.models import User
from django.db import models
from tasks import periods


class Tag(models.Model):
    user = models.ForeignKey(User)
    slug = models.SlugField()
    name = models.CharField(max_length=50)


class Task(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    description = models.TextField()
    period = models.CharField(
        max_length=30,
        choices=periods.CHOICES
    )
    count = models.IntegerField(default=1)
    tags = models.ManyToManyField(Tag)


class TaskRecord(models.Model):
    user = models.ForeignKey(User)
    task = models.ForeignKey(Task)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now=True)