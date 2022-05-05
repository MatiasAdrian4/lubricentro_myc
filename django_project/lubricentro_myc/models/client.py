from django.db import models


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
