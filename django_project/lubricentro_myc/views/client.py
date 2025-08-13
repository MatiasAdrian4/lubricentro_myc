from django.db.models import Q
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from lubricentro_myc.models.client import Cliente
from lubricentro_myc.serializers.client import (
    ClienteSerializer,
    SingleClienteSerializer,
)
from lubricentro_myc.utils import render_to_pdf
from lubricentro_myc.views.pagination import CustomPageNumberPagination


class ClienteViewSet(viewsets.ModelViewSet, CustomPageNumberPagination):
    queryset = Cliente.objects.all().order_by("id")
    serializer_class = ClienteSerializer
    pagination_class = CustomPageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = SingleClienteSerializer
        return super().retrieve(request)

    def list(self, request):
        nombre = request.GET.get("nombre")
        query = request.GET.get("query")
        if nombre:
            self.queryset = Cliente.objects.filter(nombre__icontains=nombre).order_by(
                "id"
            )
        elif query:
            self.queryset = Cliente.objects.filter(
                Q(id__contains=query) | Q(nombre__icontains=query)
            ).order_by("id")
        return super().list(request)

    @action(detail=False, methods=["get"])
    def generate_pdf(self, request):
        clients = list(self.queryset.order_by("nombre"))

        # Group clients into rows of 3
        client_rows = []
        for i in range(0, len(clients), 3):
            row = clients[i : i + 3]
            # Pad the last row with None if needed
            while len(row) < 3:
                row.append(None)
            client_rows.append(row)

        context = {
            "client_rows": client_rows,
        }
        pdf = render_to_pdf("pdf/client_pdf.html", context)
        if not pdf:
            return HttpResponse(status=500)

        response = HttpResponse(pdf, content_type="application/pdf")
        filename = "listado_de_cliente.pdf"
        content = f"inline; filename='{filename}'"
        download = request.GET.get("download")
        if download:
            content = f"attachment; filename={filename}"
        response["Content-Disposition"] = content
        return response
