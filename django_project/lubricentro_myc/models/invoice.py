from django.db import models
from django.utils import timezone
from lubricentro_myc.models.client import Cliente
from lubricentro_myc.models.product import Producto


class Remito(models.Model):
    codigo = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Remito n°{str(self.codigo)}"


class ElementoRemito(models.Model):
    remito = models.ForeignKey(Remito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.FloatField(null=False)
    pagado = models.BooleanField(default=False)
