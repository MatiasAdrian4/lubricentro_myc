from datetime import date

from django.db import models

#from lubricentro_myc.models import Venta


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
    def precio_costo_con_descuentos(self) -> float:
        return (
            self.precio_costo
            * ((100 - self.desc1) / 100)
            * ((100 - self.desc2) / 100)
            * ((100 - self.desc3) / 100)
            * ((100 - self.desc4) / 100)
        )

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

    @property
    def data(self):
        return (
            self.codigo,
            self.codigo_en_pantalla,
            self.detalle,
            self.stock,
            self.precio_costo,
            self.desc1,
            self.desc2,
            self.desc3,
            self.desc4,
            self.flete,
            self.ganancia,
            self.iva,
            self.agregado_cta_cte,
            self.categoria,
        )

    #@property
    #def amount_of_sales(self, start_date: date, end_date: date) -> float:  # or double?
    #    # TODO: consider quantity
    #    # I can aggregate quantities maybe?
    #    sales = Venta.objects.filter(
    #        producto=self, fecha__gte=start_date, fecha__lte=end_date
    #    )
    #    return 0
