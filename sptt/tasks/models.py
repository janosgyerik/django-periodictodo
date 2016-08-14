from django.contrib.auth.models import User
from django.db import models
from tasks import periods


class Tag(models.Model):
    user = models.ForeignKey(User)
    slug = models.SlugField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Task(models.Model):
    user = models.ForeignKey(User)
    period = models.CharField(
        max_length=30,
        choices=periods.CHOICES
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    count = models.IntegerField(default=1)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return '{}, {} x{}'.format(self.period, self.name, self.count)


class TaskRecord(models.Model):
    user = models.ForeignKey(User)
    task = models.ForeignKey(Task)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}, {}, {}'.format(self.user, self.task, self.created_at)
