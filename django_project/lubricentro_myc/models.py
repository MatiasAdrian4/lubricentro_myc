from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, blank=True, default='')
    localidad = models.CharField(max_length=100, blank=True, default='')
    codigo_postal = models.IntegerField(max_length=4, blank=true, default=None)
    telefono = models.IntegerField(blank=true, default=None)
    cuit = models.CharField(max_length=13, blank=True, default='')

    class __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.IntegerField(primary_key=True)
    detalle = models.CharField(max_length=200)
    stock = models.IntegerField(blank=True, default=0)
    precio_costo = models.DoubleField(blank=True, default=0.0)
    precio_venta_contado = models.DoubleField(blank=True, default=0.0)
    precio_venta_cta_cte = models.DoubleField(blank=True, default=0.0)
    categoria = models.CharField(max_length=50)

    class __str__(self):
        return self.detalle

