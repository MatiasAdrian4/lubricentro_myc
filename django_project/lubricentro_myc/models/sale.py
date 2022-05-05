from django.db import models
from django.utils import timezone
from lubricentro_myc.models.product import Producto


class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.FloatField(null=False)
    precio = models.FloatField(null=False)
    fecha = models.DateTimeField(default=timezone.now)
