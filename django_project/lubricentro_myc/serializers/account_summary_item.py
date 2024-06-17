from rest_framework import serializers

from lubricentro_myc.models import AccountSummaryItem


class AccountSummaryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSummaryItem
        fields = "__all__"
