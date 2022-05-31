from lubricentro_myc.models.client import Cliente
from lubricentro_myc.serializers.client import ClienteSerializer
from rest_framework import viewsets


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by('id')
    serializer_class = ClienteSerializer

    def list(self, request):
        nombre = request.GET.get("nombre", None)
        if nombre:
            self.queryset = Cliente.objects.filter(nombre__icontains=nombre).order_by('id')
        return super().list(request)
