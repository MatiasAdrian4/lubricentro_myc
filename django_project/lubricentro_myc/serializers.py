from rest_framework import serializers

from .models import Cliente, Producto, Remito, ElementoRemito, Venta


class ClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = ['codigo', 'detalle', 'stock', 'precio_costo', 'desc1', 'desc2', 'desc3', 'desc4', 'flete',
                  'ganancia', 'agregado_cta_cte', 'iva', 'categoria', 'precio_venta_contado', 'precio_venta_cta_cte']


class RemitoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Remito
        fields = '__all__'


class ElementoRemitoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ElementoRemito
        fields = '__all__'


class VentaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venta
        fields = '__all__'
