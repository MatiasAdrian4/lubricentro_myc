from rest_framework import serializers

from lubricentro_myc.models import Venta


class VentaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venta
        fields = '__all__'