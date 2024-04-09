import json
import traceback

from django.db.models import Q
from django.http import HttpResponse

from lubricentro_myc.models.activity import INFO, EXCEPTION
from lubricentro_myc.models.invoice import ElementoRemito, Remito
from lubricentro_myc.serializers.invoice import RemitoSerializer, UpdateRemitoSerializer
from lubricentro_myc.utils import log_activity
from lubricentro_myc.views.pagination import CustomPageNumberPagination
from rest_framework import viewsets


class RemitoViewSet(viewsets.ModelViewSet, CustomPageNumberPagination):
    queryset = Remito.objects.all().order_by("-fecha")
    serializer_class = RemitoSerializer
    pagination_class = CustomPageNumberPagination

    def list(self, request):
        nombre = request.GET.get("nombre", None)
        query = request.GET.get("query", None)
        if nombre:
            self.queryset = Remito.objects.filter(
                cliente__nombre__icontains=nombre
            ).order_by("-fecha")
        elif query:
            self.queryset = Remito.objects.filter(
                Q(cliente__nombre__icontains=query) | Q(codigo__icontains=query)
            ).order_by("-fecha")
        return super().list(request)

    def perform_create(self, serializer):
        start_activity = log_activity(
            self.request, INFO, "Invoice Creation", json.dumps(self.request.data)
        )
        try:
            remito = serializer.save()
            elementos_remito = self.request.data.get("elementos_remito")
            for elemento_remito in elementos_remito:
                ElementoRemito.objects.create(
                    remito=remito,
                    producto_id=elemento_remito.get("producto"),
                    cantidad=elemento_remito.get("cantidad"),
                )
        except:
            log_activity(
                self.request,
                EXCEPTION,
                "Invoice Creation Failed",
                traceback.format_exc(),
                start_activity,
            )
            return HttpResponse(status=500)

    def update(self, request, *args, **kwargs):
        start_activity = log_activity(
            request, INFO, "Invoice Update", json.dumps(request.data)
        )
        try:
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
        except:
            log_activity(
                request,
                EXCEPTION,
                "Invoice Update Failed",
                traceback.format_exc(),
                start_activity,
            )
            return HttpResponse(status=500)
