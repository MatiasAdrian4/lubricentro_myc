from django.db import models
from django.utils import timezone

ERROR = "error"
INFO = "info"
UNHANDLED_EXCEPTION = "unhandled_exception"

TYPE_CHOICES = [
    (ERROR, "Error"),
    (INFO, "Info"),
    (UNHANDLED_EXCEPTION, "Unhandled Exception"),
]


class Activity(models.Model):
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.TextField()
    description = models.TextField(blank=True)
