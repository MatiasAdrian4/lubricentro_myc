from rest_framework import serializers

from django_project.settings import DATE_FORMAT


class SearchClientsSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=4)


class SearchProductsSerializer(serializers.Serializer):
    detail = serializers.CharField(min_length=4, required=False)
    category = serializers.CharField(min_length=4, required=False)

    def validate(self, data):
        if not data.get("detail") and not data.get("category"):
            raise serializers.ValidationError(
                "At least one of detail or category must be present."
            )
        return data


class SearchSalesSerializer(serializers.Serializer):
    start_date = serializers.DateField(format=DATE_FORMAT, input_formats=[DATE_FORMAT])
    end_date = serializers.DateField(format=DATE_FORMAT, input_formats=[DATE_FORMAT])
