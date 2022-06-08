from lubricentro_myc.models.invoice import ElementoRemito, Remito
from rest_framework import serializers


class ElementoRemitoSinRemitoAsignado(serializers.ModelSerializer):
    class Meta:
        model = ElementoRemito
        fields = ["producto", "cantidad"]


class RemitoSerializer(serializers.ModelSerializer):
    elementos_remito = serializers.ListField(
        child=ElementoRemitoSinRemitoAsignado(), write_only=True
    )

    class Meta:
        model = Remito
        fields = [
            "codigo",
            "cliente",
            "fecha",
            "resumen_elementos",
            "esta_pago",
            "elementos_remito",
        ]

    def to_representation(self, instance):
        data = super(RemitoSerializer, self).to_representation(instance)
        data["cliente"] = instance.cliente.nombre
        return data

    def create(self, validated_data):
        validated_data.pop("elementos_remito")
        return super(RemitoSerializer, self).create(validated_data)
