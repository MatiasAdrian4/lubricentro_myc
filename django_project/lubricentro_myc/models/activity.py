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
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    request = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.TextField()
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
