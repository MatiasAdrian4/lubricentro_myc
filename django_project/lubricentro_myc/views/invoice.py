from django.db.models import Q
from django.http import HttpResponse
from lubricentro_myc.models.invoice import ElementoRemito, Remito
from lubricentro_myc.serializers.invoice import RemitoSerializer, UpdateRemitoSerializer
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

    def update(self, request, *args, **kwargs):
        serializer = UpdateRemitoSerializer(
            data=request.data, context={"invoice_id": kwargs["pk"]}
        )
        serializer.is_valid(raise_exception=True)

        invoice_items_to_update = ElementoRemito.objects.filter(
            remito_id=kwargs["pk"],
            id__in=[
                invoice_item["id"]
                for invoice_item in serializer.data.get("elementos_remito")
            ],
        )
        invoice_items_to_delete = ElementoRemito.objects.filter(
            Q(remito_id=kwargs["pk"])
            & ~Q(
                id__in=[
                    invoice_item["id"]
                    for invoice_item in serializer.data.get("elementos_remito")
                ]
            )
        )

        if invoice_items_to_update.count() > 0:
            new_quantities = {
                invoice_item["id"]: invoice_item["cantidad"]
                for invoice_item in serializer.data.get("elementos_remito")
            }
            for invoice_item in invoice_items_to_update:
                invoice_item.cantidad = new_quantities[invoice_item.id]
                invoice_item.save()

        invoice_items_to_delete.delete()

        return HttpResponse(status=200)
