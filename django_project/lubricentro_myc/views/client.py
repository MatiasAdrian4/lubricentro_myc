from django.http import JsonResponse
from lubricentro_myc.models import Cliente
from lubricentro_myc.serializers.client import ClienteSerializer
from rest_framework import viewsets
from rest_framework.decorators import action


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    @action(detail=False, methods=["get"])
    def buscar(self, request):
        resultado = []
        nombre = request.GET.get("nombre", None)
        if nombre:
            for cliente in Cliente.objects.filter(nombre__icontains=nombre).values():
                resultado.append(
                    {
                        "codigo": cliente.get("id", ""),
                        "nombre": cliente.get("nombre", ""),
                    }
                )
        return JsonResponse(data={"clientes": resultado})
