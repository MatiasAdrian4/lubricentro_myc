from rest_framework import serializers

from django_project.settings import DATE_FORMAT

BEST = "best"
WORST = "worst"


class BestAndWorstSellingProductsRequestSerializer(serializers.Serializer):
    start_date = serializers.DateField(format=DATE_FORMAT, input_formats=[DATE_FORMAT])
    end_date = serializers.DateField(format=DATE_FORMAT, input_formats=[DATE_FORMAT])
    type = serializers.ChoiceField(choices=[BEST, WORST])
    limit = serializers.IntegerField(min_value=1, max_value=100, default=10)


class BestAndWorstSellingProductsResponseSerializer(serializers.Serializer):
    pass
