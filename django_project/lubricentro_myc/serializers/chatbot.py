from rest_framework import serializers


class SearchClientsSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=4)
