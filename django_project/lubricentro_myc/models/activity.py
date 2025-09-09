from django.db import models
from django.utils import timezone

EXCEPTION = "exception"
INFO = "info"
UNHANDLED_EXCEPTION = "unhandled_exception"

TYPE_CHOICES = [
    (EXCEPTION, "Exception"),
    (INFO, "Info"),
    (UNHANDLED_EXCEPTION, "Unhandled Exception"),
]


class Activity(models.Model):
    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE
    )  # TODO: make it optional
    request = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.TextField()
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, related_name="parent_activity"
    )
