from django.db import models
from tasks import periods


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    period = models.CharField(
        max_length=10,
        choices=periods.CHOICES
    )
