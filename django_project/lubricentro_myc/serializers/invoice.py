from lubricentro_myc.models.invoice import ElementoRemito, Remito
from rest_framework import serializers


class RemitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remito
        fields = ["codigo", "cliente", "fecha", "resumen_elementos"]

    def to_representation(self, instance):
        data = super(RemitoSerializer, self).to_representation(instance)
        data["cliente"] = instance.cliente.nombre
        return data


class ElementoRemitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElementoRemito
        fields = "__all__"
