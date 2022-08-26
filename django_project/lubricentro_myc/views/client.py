from django.db.models import Q
from lubricentro_myc.models.client import Cliente
from lubricentro_myc.serializers.client import (
    ClienteSerializer,
    SingleClienteSerializer,
)
from lubricentro_myc.views.pagination import CustomPageNumberPagination
from rest_framework import viewsets


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
