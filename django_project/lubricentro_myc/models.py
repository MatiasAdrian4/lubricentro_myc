from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, blank=True, default='')
    localidad = models.CharField(max_length=100, blank=True, default='')
    codigo_postal = models.CharField(max_length=4, blank=True, default="")
    telefono = models.CharField(max_length=13, blank=True, default="")
    cuit = models.CharField(max_length=13, blank=True, default='')

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.AutoField(primary_key=True)
    detalle = models.CharField(max_length=200)
    stock = models.IntegerField(default=0)
    precio_costo = models.FloatField(default=0.0)
    precio_venta_contado = models.FloatField(default=0.0)
    precio_venta_cta_cte = models.FloatField(default=0.0)
    categoria = models.CharField(max_length=50)
    desc1 = models.FloatField(default=0.0)
    desc2 = models.FloatField(default=0.0)
    desc3 = models.FloatField(default=0.0)
    desc4 = models.FloatField(default=0.0)

    def __str__(self):
        return self.detalle

class ElementoRemito(models.Model):
    numero_remito = models.IntegerField(null=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=False)

    def __str__(self):
        return self.numero_remito


