from django.db import models
from django.utils import timezone


class Venta(models.Model):
    producto = models.ForeignKey("lubricentro_myc.Producto", on_delete=models.CASCADE)
    cantidad = models.FloatField(null=False)
    precio = models.FloatField(null=False)
    fecha = models.DateTimeField(default=timezone.now)

    @property
    def data(self):
        return self.id, self.producto.codigo, self.cantidad, self.precio, self.fecha
