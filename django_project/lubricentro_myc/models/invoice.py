from django.db import models
from django.utils import timezone
from lubricentro_myc.models.invoice_item import ElementoRemito


class Remito(models.Model):
    codigo = models.AutoField(primary_key=True)
    cliente = models.ForeignKey("lubricentro_myc.Cliente", on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Remito n°{str(self.codigo)}"

    @property
    def resumen_elementos(self) -> str:
        elementos_remito = ElementoRemito.objects.filter(remito_id=self.codigo)
        resumen_elementos = ""
        for elemento in elementos_remito:
            resumen_elementos += f"{elemento.cantidad} und. - {elemento.producto.codigo} ({elemento.producto.detalle});"
        return resumen_elementos[:-1]

    @property
    def esta_pago(self) -> bool:
        elementos_remito_no_pagos = ElementoRemito.objects.filter(
            remito_id=self.codigo, pagado=False
        )
        return True if len(elementos_remito_no_pagos) == 0 else False
