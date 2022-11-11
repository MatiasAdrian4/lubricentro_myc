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
    def resumen_elementos(self):
        return [
            {
                "id": elemento.id,
                "producto": {
                    "codigo": elemento.producto.codigo_en_pantalla,
                    "detalle": elemento.producto.detalle,
                },
                "cantidad": elemento.cantidad,
                "pagado": elemento.pagado,
            }
            for elemento in ElementoRemito.objects.filter(remito_id=self.codigo)
        ]

    @property
    def esta_pago(self) -> bool:
        elementos_remito_no_pagos = ElementoRemito.objects.filter(
            remito_id=self.codigo, pagado=False
        )
        return len(elementos_remito_no_pagos) == 0
