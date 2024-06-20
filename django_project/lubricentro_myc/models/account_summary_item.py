from django.db import models
from django.utils import timezone

DEBE = "debe"
HABER = "haber"

TYPE_CHOICES = [
    (DEBE, "Debe"),
    (HABER, "Haber"),
]


class AccountSummaryItem(models.Model):
    client = models.ForeignKey("lubricentro_myc.Cliente", on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.FloatField(null=False)

    @property
    def data(self):
        return (
            self.id,
            self.client.id,
            self.date,
            self.description,
            self.type,
            self.amount,
        )
