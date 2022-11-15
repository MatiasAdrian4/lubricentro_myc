import json

from django.db.models import Q
from django.http import HttpResponse
from lubricentro_myc.models import Venta
from lubricentro_myc.models.invoice import ElementoRemito
from lubricentro_myc.serializers.invoice_item import (
    BillingSerializer,
    ElementoRemitoSerializer,
)
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
            filters &= Q(pagado=json.loads(pago))
        if filters:
            self.queryset = ElementoRemito.objects.filter(filters).order_by("id")
        return super().list(request)

    def update(self, request, *args, **kwargs):
        remito = request.data.get("remito", None)
        producto = request.data.get("producto", None)
        if remito or producto:
            return HttpResponse(status=400)
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=["post"])
    def bulk(self, request):
        serializer = BillingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for invoice_item in ElementoRemito.objects.filter(
            id__in=serializer.data["items"]
        ):
            invoice_item.pagado = True
            invoice_item.save()
            # save sale without updating stock
            Venta.objects.create(
                producto=invoice_item.producto,
                cantidad=invoice_item.cantidad,
                precio=(
                    invoice_item.producto.precio_venta_cta_cte * invoice_item.cantidad
                ),
            )
        return HttpResponse(status=200)
