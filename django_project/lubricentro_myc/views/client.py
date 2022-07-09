from lubricentro_myc.models.client import Cliente
from lubricentro_myc.serializers.client import (
    ClienteSerializer,
    SingleClienteSerializer,
)
from rest_framework import viewsets


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by("id")
    serializer_class = ClienteSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = SingleClienteSerializer
        return super().retrieve(request)

    def list(self, request):
        nombre = request.GET.get("nombre")
        if nombre:
            self.queryset = Cliente.objects.filter(nombre__icontains=nombre).order_by(
                "id"
            )
        return super().list(request)
