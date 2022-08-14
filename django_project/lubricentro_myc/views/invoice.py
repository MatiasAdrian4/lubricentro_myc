from lubricentro_myc.models.invoice import ElementoRemito, Remito
from lubricentro_myc.serializers.invoice import RemitoSerializer
from lubricentro_myc.views.pagination import CustomPageNumberPagination
from rest_framework import viewsets


class RemitoViewSet(viewsets.ModelViewSet, CustomPageNumberPagination):
    queryset = Remito.objects.all().order_by("-fecha")
    serializer_class = RemitoSerializer
    pagination_class = CustomPageNumberPagination

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
            ElementoRemito.objects.create(
                remito=remito,
                producto_id=elemento_remito.get("producto"),
                cantidad=elemento_remito.get("cantidad"),
            )
