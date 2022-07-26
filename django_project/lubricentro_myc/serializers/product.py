from lubricentro_myc.models.product import Producto
from rest_framework import serializers


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            "codigo_en_pantalla",
            "detalle",
            "stock",
            "precio_costo",
            "desc1",
            "desc2",
            "desc3",
            "desc4",
            "flete",
            "ganancia",
            "iva",
            "agregado_cta_cte",
            "categoria",
            "precio_venta_contado",
            "precio_venta_cta_cte",
        ]

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        codigo_en_pantalla = validated_data.get("codigo_en_pantalla")
        if not codigo_en_pantalla:
            instance.codigo_en_pantalla = instance.codigo
            instance.save()
        return instance

    def to_representation(self, instance):
        data = super(ProductoSerializer, self).to_representation(instance)
        data["precio_costo"] = round(instance.precio_costo, 2)
        return data
