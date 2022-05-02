from django.db import models
from django.utils import timezone


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
    def precio_costo_con_descuentos(self):
        return (
            self.precio_costo
            * ((100 - self.desc1) / 100)
            * ((100 - self.desc2) / 100)
            * ((100 - self.desc3) / 100)
            * ((100 - self.desc4) / 100)
        )

    @property
    def precio_venta_contado(self):
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
        return int(precio_total_con_ganancias)

    @property
    def precio_venta_cta_cte(self):
        return int(self.precio_venta_contado * ((100 + self.agregado_cta_cte) / 100))


class Remito(models.Model):
    codigo = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Remito n°" + str(self.codigo)


class ElementoRemito(models.Model):
    remito = models.ForeignKey(Remito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.FloatField(null=False)
    pagado = models.BooleanField(default=False)


class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.FloatField(null=False)
    precio = models.FloatField(null=False)
    fecha = models.DateTimeField(default=timezone.now)
