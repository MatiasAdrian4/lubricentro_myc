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

    @property
    def resumen_elementos(self) -> str:
        elementos_remito = ElementoRemito.objects.filter(remito_id=self.codigo)
        resumen_elementos = ""
        for elemento in elementos_remito:
            resumen_elementos += f"{elemento.producto.codigo} ({elemento.producto.detalle}) - {elemento.cantidad} und.;"
        return resumen_elementos[:-1]

    @property
    def esta_pago(self) -> bool:
        elementos_remito_no_pagos = ElementoRemito.objects.filter(
            remito_id=self.codigo, pagado=False
        )
        return True if len(elementos_remito_no_pagos) == 0 else False


class ElementoRemito(models.Model):
    remito = models.ForeignKey(Remito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.FloatField(null=False)
    pagado = models.BooleanField(default=False)
