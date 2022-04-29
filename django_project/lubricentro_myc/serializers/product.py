from rest_framework import serializers

from lubricentro_myc.models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            "codigo",
            "detalle",
            "stock",
            "precio_costo",
            "desc1",
            "desc2",
            "desc3",
            "desc4",
            "flete",
            "ganancia",
            "agregado_cta_cte",
            "iva",
            "categoria",
            "precio_venta_contado",
            "precio_venta_cta_cte",
        ]
