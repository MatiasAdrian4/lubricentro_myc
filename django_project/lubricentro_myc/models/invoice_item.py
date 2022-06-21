from django.db import models


class ElementoRemito(models.Model):
    remito = models.ForeignKey("lubricentro_myc.Remito", on_delete=models.CASCADE)
    producto = models.ForeignKey("lubricentro_myc.Producto", on_delete=models.CASCADE)
    cantidad = models.FloatField(null=False)
    pagado = models.BooleanField(default=False)
