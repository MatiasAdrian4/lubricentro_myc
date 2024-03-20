from lubricentro_myc.models.invoice import ElementoRemito, Remito
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UpdateElementoRemitoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = ElementoRemito
        fields = ["id", "cantidad"]


class UpdateRemitoSerializer(serializers.Serializer):
    elementos_remito = serializers.ListField(child=UpdateElementoRemitoSerializer())

    def validate(self, data):
        invoice_id = self.context.get("invoice_id")
        if ElementoRemito.objects.filter(remito_id=invoice_id, pagado=True).count() > 0:
            raise ValidationError(
                "Remito no puede ser actualizado dado que 1 o mas Elementos de Remito ya estan pagos."
            )
        return data


class GetElementoRemitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElementoRemito
        fields = ["producto", "cantidad"]


class RemitoSerializer(serializers.ModelSerializer):
    elementos_remito = serializers.ListField(
        child=GetElementoRemitoSerializer(), write_only=True
    )

    class Meta:
        model = Remito
        fields = [
            "codigo",
            "cliente",
            "fecha",
            "resumen_elementos",
            "esta_pago",
            "elementos_remito",
        ]

    def to_representation(self, instance):
        data = super(RemitoSerializer, self).to_representation(instance)
        data["cliente"] = {
            "id": instance.cliente.id,
            "nombre": instance.cliente.nombre
        }
        return data

    def create(self, validated_data):
        validated_data.pop("elementos_remito")
        return super(RemitoSerializer, self).create(validated_data)
