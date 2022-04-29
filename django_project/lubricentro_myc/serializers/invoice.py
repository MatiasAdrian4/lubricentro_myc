from rest_framework import serializers

from lubricentro_myc.models import Remito, ElementoRemito


class RemitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remito
        fields = "__all__"


class ElementoRemitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElementoRemito
        fields = "__all__"
