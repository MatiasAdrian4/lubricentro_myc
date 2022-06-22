from django.db import models
from lubricentro_myc.models.invoice import ElementoRemito


class Cliente(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=100, blank=True, default="")
    localidad = models.CharField(max_length=100, blank=True, default="")
    codigo_postal = models.CharField(max_length=4, blank=True, default="")
    telefono = models.CharField(max_length=13, blank=True, default="")
    cuit = models.CharField(max_length=13, blank=True, default="")
    email = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return self.nombre

    @property
    def deuda_actual(self):
        actual_price = 0
        for invoice_item in ElementoRemito.objects.filter(
            remito__cliente_id=self.id, pagado=False
        ):
            actual_price += (
                invoice_item.producto.precio_venta_cta_cte * invoice_item.cantidad
            )
        return actual_price
