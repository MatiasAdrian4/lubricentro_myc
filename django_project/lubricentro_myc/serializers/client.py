from lubricentro_myc.models.client import Cliente
from lubricentro_myc.serializers.invoice import RemitoSerializer
from rest_framework import serializers


class SingleClienteSerializer(serializers.ModelSerializer):
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


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"
