from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from lubricentro_myc.models import Cliente
from lubricentro_myc.serializers.client import ClienteSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    @action(detail=False, methods=['get'])
    def buscar(self, request):
        resultado = []
        nombre = request.GET.get('nombre', '')
        if nombre == '':
            return JsonResponse(data={'clientes': resultado})
        for cliente in Cliente.objects.filter(nombre__icontains=nombre).values():
            resultado.append({
                "codigo": cliente['id'],
                "nombre": cliente['nombre']
            })
        return JsonResponse(data={'clientes': resultado})