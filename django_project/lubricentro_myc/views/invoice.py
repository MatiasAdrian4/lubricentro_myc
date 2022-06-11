from django.http import HttpResponse
from lubricentro_myc.models.invoice import ElementoRemito, Remito
from lubricentro_myc.models.product import Producto
from lubricentro_myc.serializers.invoice import RemitoSerializer
from rest_framework import viewsets
from rest_framework.decorators import action


class RemitoViewSet(viewsets.ModelViewSet):
    queryset = Remito.objects.all().order_by("-fecha")
    serializer_class = RemitoSerializer

    def list(self, request):
        nombre = request.GET.get("nombre", None)
        if nombre:
            self.queryset = Remito.objects.filter(
                cliente__nombre__icontains=nombre
            ).order_by("-fecha")
        return super().list(request)

    def perform_create(self, serializer):
        remito = serializer.save()
        elementos_remito = self.request.data.get("elementos_remito")
        for elemento_remito in elementos_remito:
            producto = Producto.objects.get(codigo=elemento_remito.get("producto"))
            producto.stock -= elemento_remito.get("cantidad")
            ElementoRemito.objects.create(
                remito=remito,
                producto=producto,
                cantidad=elemento_remito.get("cantidad"),
            )
            producto.save()
