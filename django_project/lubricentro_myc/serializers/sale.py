from lubricentro_myc.models.sale import Venta
from rest_framework import serializers


class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = "__all__"

    def to_representation(self, instance):
        data = super(VentaSerializer, self).to_representation(instance)
        data["producto"] = {
            "codigo": instance.producto.codigo,
            "detalle": instance.producto.detalle,
        }
        return data


class VentasSerializer(serializers.Serializer):
    ventas = serializers.ListField(child=VentaSerializer())
