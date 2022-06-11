from django.db.models import Q
from django.http import HttpResponse
from lubricentro_myc.models.invoice import ElementoRemito, Remito
from lubricentro_myc.models.product import Producto
from lubricentro_myc.serializers.invoice_item import ElementoRemitoSerializer
from rest_framework import viewsets
from rest_framework.decorators import action


class ElementoRemitoViewSet(viewsets.ModelViewSet):
    queryset = ElementoRemito.objects.all().order_by("id")
    serializer_class = ElementoRemitoSerializer
    pagination_class = None

    def list(self, request):
        codigo_cliente = request.GET.get("codigo_cliente", None)
        pago = request.GET.get("pago", None)
        filters = Q()
        if codigo_cliente:
            filters &= Q(remito__cliente=codigo_cliente)
        if pago:
            filters &= Q(pagado=pago)
        if filters:
            self.queryset = ElementoRemito.objects.filter(filters).order_by("id")
        return super().list(request)

    @action(methods=["post"], detail=False)
    def marcar_pagados(self, request):
        elemento_ids = request.data.get("elementos")
        if not elemento_ids:
            return HttpResponse(status=400)
        ElementoRemito.objects.filter(id__in=elemento_ids).update(pagado=True)
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
                if nueva_cantidad != 0:
                    elemento_remito.cantidad = nueva_cantidad
                    elemento_remito.save()
                else:
                    elemento_remito.delete()
            elif nueva_cantidad > elemento_remito.cantidad:
                producto.stock -= nueva_cantidad - elemento_remito.cantidad
                producto.save()
                if nueva_cantidad != 0:
                    elemento_remito.cantidad = nueva_cantidad
                    elemento_remito.save()
                else:
                    elemento_remito.delete()
        return HttpResponse(status=200)
