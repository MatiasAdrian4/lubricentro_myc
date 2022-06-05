from django.http import HttpResponse, JsonResponse
from lubricentro_myc.models.invoice import ElementoRemito, Remito
from lubricentro_myc.models.product import Producto
from lubricentro_myc.serializers.invoice import (
    ElementoRemitoSerializer,
    RemitoSerializer,
)
from rest_framework import viewsets
from rest_framework.decorators import action


class RemitoViewSet(viewsets.ModelViewSet):
    queryset = Remito.objects.all().order_by("-fecha")
    serializer_class = RemitoSerializer

    @action(detail=False, methods=["get"])
    def borrar_remito(self, request):
        codigo = request.GET.get("codigo")
        if not codigo:
            return HttpResponse(status=400)
        try:
            remito = Remito.objects.get(codigo=codigo)
        except Remito.DoesNotExist:
            return HttpResponse(status=404)
        elementos_remito = ElementoRemito.objects.filter(remito=codigo)
        for elemento_remito in elementos_remito:
            producto = Producto.objects.get(codigo=elemento_remito.producto.codigo)
            producto.stock += elemento_remito.cantidad
            producto.save()
        elementos_remito.delete()
        remito.delete()
        return HttpResponse(status=200)


class ElementoRemitoViewSet(viewsets.ModelViewSet):
    queryset = ElementoRemito.objects.all().order_by("id")
    serializer_class = ElementoRemitoSerializer

    @action(detail=False, methods=["get"])
    def buscar_por_codigo_cliente(self, request):
        codigo = request.GET.get("codigo")
        if not codigo:
            return HttpResponse(status=400)
        resultado = []
        for elem in ElementoRemito.objects.filter(remito__cliente=codigo, pagado=False):
            try:
                prod = Producto.objects.get(codigo=elem.producto_id)
                resultado.append(
                    {
                        "elem_remito": elem.id,
                        "remito": elem.remito.codigo,
                        "codigo_producto": prod.codigo,
                        "detalle": prod.detalle,
                        "precio_cta_cte": prod.precio_venta_cta_cte,
                        "cantidad": elem.cantidad,
                    }
                )
            except Producto.DoesNotExist:
                continue
        return JsonResponse(data={"elementos_remito": resultado})

    @action(methods=["post"], detail=False)
    def marcar_pagados(self, request):
        elem_ids = request.data.get("elementos")
        if not elem_ids:
            return HttpResponse(status=400)
        for elem_id in elem_ids:
            try:
                elem_remito = ElementoRemito.objects.get(id=elem_id)
                elem_remito.pagado = True
                elem_remito.save()
            except ElementoRemito.DoesNotExist:
                continue
        return HttpResponse(status=200)

    @action(methods=["post"], detail=False)
    def guardar_elementos(self, request):
        elementos = request.data.get("elementos")
        if not elementos:
            return HttpResponse(status=400)
        for elem in elementos:
            try:
                producto = Producto.objects.get(codigo=elem.get("producto"))
                remito = Remito.objects.get(codigo=elem.get("remito"))
                producto.stock -= float(elem.get("cantidad"))
                producto.save()
                new_elem = ElementoRemito(
                    remito=remito,
                    producto=producto,
                    cantidad=elem["cantidad"],
                    pagado=False,
                )
                new_elem.save()
            except (Producto.DoesNotExist, Remito.DoesNotExist):
                continue
        return HttpResponse(status=200)

    @action(detail=False, methods=["post"])
    def modificar_cantidad(self, request):  # test this
        elementos = request.data.get("elementos")
        if not elementos:
            return HttpResponse(status=400)
        for elem in elementos:
            nueva_cantidad = float(elem.get("cantidad"))
            try:
                elemento_remito = ElementoRemito.objects.get(id=elem.get("id"))
                producto = Producto.objects.get(codigo=elemento_remito.producto.codigo)
            except (ElementoRemito.DoesNotExist, Producto.DoesNotExist):
                continue
            if nueva_cantidad < elemento_remito.cantidad:
                producto.stock += elemento_remito.cantidad - nueva_cantidad
                producto.save()
                elemento_remito.cantidad = nueva_cantidad
                elemento_remito.save()
            elif nueva_cantidad > elemento_remito.cantidad:
                producto.stock -= nueva_cantidad - elemento_remito.cantidad
                producto.save()
                elemento_remito.cantidad = nueva_cantidad
                elemento_remito.save()
            else:  # nueva_cantidad == 0
                elemento_remito.delete()
        return HttpResponse(status=200)
