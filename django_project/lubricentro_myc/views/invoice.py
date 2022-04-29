from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from lubricentro_myc.models import Remito, ElementoRemito, Producto
from lubricentro_myc.serializers.invoice import (
    RemitoSerializer,
    ElementoRemitoSerializer,
)


class RemitoViewSet(viewsets.ModelViewSet):
    queryset = Remito.objects.all()
    serializer_class = RemitoSerializer

    @action(detail=False, methods=["get"])
    def borrar_remito(self, request):
        codigo = request.GET.get("codigo", "")
        elementos_remito = ElementoRemito.objects.filter(remito=codigo)
        for elemento_remito in elementos_remito:
            producto = Producto.objects.get(codigo=elemento_remito.producto.codigo)
            producto.stock += float(elemento_remito.cantidad)
            producto.save()
        elementos_remito.delete()
        remito = Remito.objects.get(codigo=codigo)
        remito.delete()
        return HttpResponse(status=200)


class ElementoRemitoViewSet(viewsets.ModelViewSet):
    queryset = ElementoRemito.objects.all()
    serializer_class = ElementoRemitoSerializer

    @action(detail=False, methods=["get"])
    def buscar(self, request):
        codigo = request.GET.get("codigo", "")
        elementos_remito = ElementoRemito.objects.filter(
            remito__cliente=codigo, pagado=False
        )
        resultado = []
        for elem in elementos_remito:
            prod = Producto.objects.get(codigo=elem.producto_id)
            resultado.append(
                {
                    "elem_remito": elem.id,
                    "remito": elem.remito.codigo,
                    "codigo": prod.codigo,
                    "detalle": prod.detalle,
                    "precio_cta_cte": prod.precio_venta_cta_cte,
                    "cantidad": elem.cantidad,
                }
            )
        return JsonResponse(data={"elementos_remito": resultado})

    @action(methods=["post"], detail=False)
    def marcar_pagado(self, request):
        elems = self.request.data["elementos"]
        for elem in elems:
            elem_remito = ElementoRemito.objects.get(id=elem["id"])
            elem_remito.pagado = True
            elem_remito.save()
        return HttpResponse(status=200)

    @action(methods=["post"], detail=False)
    def guardar_elementos(self, request):
        elems = self.request.data["elementos"]
        for elem in elems:
            producto = Producto.objects.get(codigo=elem["producto"])
            producto.stock -= float(elem["cantidad"])
            producto.save()
            new_elem = ElementoRemito(
                remito=Remito.objects.get(codigo=elem["remito"]),
                producto=producto,
                cantidad=elem["cantidad"],
                pagado=False,
            )
            new_elem.save()
        return HttpResponse(status=200)

    @action(detail=False, methods=["post"])
    def modificar(self, request):
        elementos = self.request.data["elementos"]
        for elem in elementos:
            nueva_cantidad = float(elem["cantidad"])
            elemento_remito = ElementoRemito.objects.get(id=elem["id"])
            if nueva_cantidad < elemento_remito.cantidad:
                producto = Producto.objects.get(codigo=elemento_remito.producto.codigo)
                producto.stock += elemento_remito.cantidad - nueva_cantidad
                producto.save()
                if nueva_cantidad != 0:
                    elemento_remito.cantidad = nueva_cantidad
                    elemento_remito.save()
                else:
                    elemento_remito.delete()
            elif nueva_cantidad > elemento_remito.cantidad:
                producto = Producto.objects.get(codigo=elemento_remito.producto.codigo)
                producto.stock -= nueva_cantidad - elemento_remito.cantidad
                producto.save()
                if nueva_cantidad != 0:
                    elemento_remito.cantidad = nueva_cantidad
                    elemento_remito.save()
                else:
                    elemento_remito.delete()
        return HttpResponse(status=200)
