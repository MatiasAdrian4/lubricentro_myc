from lubricentro_myc.models.product import Producto
from rest_framework import serializers


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = "__all__"

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        codigo_en_pantalla = validated_data.get("codigo_en_pantalla")
        if not codigo_en_pantalla:
            instance.codigo_en_pantalla = instance.codigo
            instance.save()
        return instance


