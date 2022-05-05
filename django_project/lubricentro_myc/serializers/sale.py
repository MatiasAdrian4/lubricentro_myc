from django.utils import timezone
from lubricentro_myc.models import Venta
from rest_framework import serializers


class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = "__all__"


class VentasSerializer(serializers.Serializer):
    ventas = serializers.ListField(child=VentaSerializer())
