from dateutil import parser
from django.db.models import Q

from django.http import HttpResponse
from rest_framework import viewsets

from lubricentro_myc.models import AccountSummaryItem
from lubricentro_myc.serializers.account_summary_item import (
    AccountSummaryItemSerializer,
)


class AccountSummaryItemViewSet(viewsets.ModelViewSet):
    queryset = AccountSummaryItem.objects.all().order_by("date")
    serializer_class = AccountSummaryItemSerializer
    pagination_class = None

    def list(self, request):
        client_id = request.GET.get("client_id")

        if not client_id:
            return HttpResponse(status=400)

        filters = Q(client__id=client_id)

        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if start_date and end_date:
            try:
                start_date = parser.parse(start_date)
                end_date = parser.parse(end_date)
            except ValueError:
                return HttpResponse(status=400)

            filters &= Q(date__date__gte=start_date)
            filters &= Q(date__date__lte=end_date)

        elif (start_date and not end_date) or (not start_date and end_date):
            return HttpResponse(status=400)

        self.queryset = AccountSummaryItem.objects.filter(filters).order_by("date")
        return super().list(request)
