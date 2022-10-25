from django.db import models


class ProductCostHistory(models.Model):
    product = models.ForeignKey("lubricentro_myc.Producto", on_delete=models.CASCADE)
    old_price = models.FloatField()
    new_price = models.FloatField()
    timestamp = models.DateTimeField()
