from rest_framework import serializers

from .models import Cliente, Producto, Remito, ElementoRemito

class ClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = '__all__'


class RemitoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Remito
        fields = '__all__'

class ElementoRemitoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ElementoRemito
        fields = '__all__'