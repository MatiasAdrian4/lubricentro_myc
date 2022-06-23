from lubricentro_myc.models.client import Cliente
from rest_framework import serializers

from lubricentro_myc.serializers.invoice import RemitoSerializer


class ClienteSerializer(serializers.ModelSerializer):
    lista_remitos = serializers.ListField(child=RemitoSerializer(), read_only=True)

    class Meta:
        model = Cliente
        fields = [
            "id",
            "nombre",
            "direccion",
            "localidad",
            "codigo_postal",
            "telefono",
            "cuit",
            "email",
            "lista_remitos",
            "deuda_actual",
        ]
