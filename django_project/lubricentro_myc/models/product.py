from django.db import models


class Producto(models.Model):
    codigo = models.AutoField(primary_key=True)
    codigo_en_pantalla = models.IntegerField(null=True, unique=True)
    detalle = models.CharField(max_length=200)
    stock = models.FloatField(default=0.0)
    precio_costo = models.FloatField(default=0.0)  # sin iva
    desc1 = models.FloatField(default=0.0)
    desc2 = models.FloatField(default=0.0)
    desc3 = models.FloatField(default=0.0)
    desc4 = models.FloatField(default=0.0)
    flete = models.FloatField(default=0.0)
    ganancia = models.FloatField(default=40.0)
    iva = models.FloatField(default=21.0)
    agregado_cta_cte = models.FloatField(default=0.0)
    categoria = models.CharField(max_length=50)

    def __str__(self):
        return self.detalle

    @property
    def precio_venta_contado(self) -> float:
        precio_total_con_descuentos = (
            self.precio_costo
            * ((100 - self.desc1) / 100)
            * ((100 - self.desc2) / 100)
            * ((100 - self.desc3) / 100)
            * ((100 - self.desc4) / 100)
        )
        precio_total_con_ganancias = (
            precio_total_con_descuentos
            * ((100 + self.flete) / 100)
            * ((100 + self.ganancia) / 100)
            * ((100 + self.iva) / 100)
        )
        return round(precio_total_con_ganancias, 2)

    @property
    def precio_venta_cta_cte(self) -> float:
        return round(
            self.precio_venta_contado * ((100 + self.agregado_cta_cte) / 100), 2
        )
