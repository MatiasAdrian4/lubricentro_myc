from django.db.models import Q
from django.http import HttpResponse
from lubricentro_myc.models.invoice import ElementoRemito
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

    def update(self, request, *args, **kwargs):
        remito = request.data.get("remito", None)
        producto = request.data.get("producto", None)
        if remito or producto:
            return HttpResponse(status=400)
        return super().update(request, *args, **kwargs)
