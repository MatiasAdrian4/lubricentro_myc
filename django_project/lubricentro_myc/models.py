from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, blank=True, default='')
    localidad = models.CharField(max_length=100, blank=True, default='')
    codigo_postal = models.IntegerField(blank=True, default=None)
    telefono = models.IntegerField(blank=True, default=None)
    cuit = models.CharField(max_length=13, blank=True, default='')

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.AutoField(primary_key=True)
    detalle = models.CharField(max_length=200)
    stock = models.IntegerField(blank=True, default=0)
    precio_costo = models.FloatField(blank=True, default=0.0)
    precio_venta_contado = models.FloatField(blank=True, default=0.0)
    precio_venta_cta_cte = models.FloatField(blank=True, default=0.0)
    categoria = models.CharField(max_length=50)
    desc1 = models.FloatField(blank=True, default=0.0)
    desc2 = models.FloatField(blank=True, default=0.0)
    desc3 = models.FloatField(blank=True, default=0.0)
    desc4 = models.FloatField(blank=True, default=0.0)

    def __str__(self):
        return self.detalle

