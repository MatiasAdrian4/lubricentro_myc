import os
from lubricentro_myc.models import Producto


def leer_archivo(archivo):
    productos = open(archivo, "r")
    for producto in productos:
        i = 0
        aux = ""
        valores = []
        for it in range(7):
            while producto[i] == '@':
                i += 1
            while producto[i] != '@':
                aux += producto[i]
                i += 1
            valores.append(aux)
            aux = ""
        p = Producto(
            codigo=valores[0],
            detalle=valores[1][1:len(valores[1])-1],
            stock=0,
            precio_costo=valores[3],
            precio_venta_contado=valores[5],
            precio_venta_cta_cte=valores[5],
            categoria=productos.name[27:len(
                productos.name)-4].replace("_", " ")
        )
        p.save()


def run():
    for filename in os.listdir(os.getcwd()+'/django_project/scripts/txt/'):
        leer_archivo('django_project/scripts/txt/'+filename)
