from lubricentro_myc.models.invoice import ElementoRemito
from rest_framework import serializers


class ElementoRemitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElementoRemito
        fields = "__all__"

    def to_representation(self, instance):
        data = super(ElementoRemitoSerializer, self).to_representation(instance)
        data["producto"] = {
            "codigo": instance.producto.codigo,
            "detalle": instance.producto.detalle,
            "precio_venta_cta_cte": instance.producto.precio_venta_cta_cte,
        }
        return data


class BillingSerializer(serializers.Serializer):
    items = serializers.PrimaryKeyRelatedField(
        queryset=ElementoRemito.objects.filter(pagado=False), many=True
    )
