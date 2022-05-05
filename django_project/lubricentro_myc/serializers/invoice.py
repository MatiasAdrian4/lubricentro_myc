from lubricentro_myc.models.invoice import ElementoRemito, Remito
from rest_framework import serializers


class RemitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remito
        fields = "__all__"


class ElementoRemitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElementoRemito
        fields = "__all__"
