from rest_framework import serializers

from django_project.settings import DATE_FORMAT


class SearchClientsSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=4)


class SearchSalesSerializer(serializers.Serializer):
    start_date = serializers.DateField(format=DATE_FORMAT, input_formats=[DATE_FORMAT])
    end_date = serializers.DateField(format=DATE_FORMAT, input_formats=[DATE_FORMAT])
