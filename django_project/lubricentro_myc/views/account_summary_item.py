from dateutil import parser
from django.db.models import Q

from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError

from lubricentro_myc.models import AccountSummaryItem, Cliente
from lubricentro_myc.models.account_summary_item import DEBE
from lubricentro_myc.serializers.account_summary_item import (
    AccountSummaryItemSerializer,
)
from lubricentro_myc.utils import render_to_pdf


class AccountSummaryItemViewSet(viewsets.ModelViewSet):
    queryset = AccountSummaryItem.objects.all().order_by("date")
    serializer_class = AccountSummaryItemSerializer
    pagination_class = None

    def get_params_from_request(self, request):
        client_id = request.GET.get("client_id")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if not client_id or not start_date or not end_date:
            raise ParseError()

        try:
            start_date = parser.parse(start_date)
            end_date = parser.parse(end_date)
        except ValueError:
            raise ParseError()

        return client_id, start_date, end_date

    def get_filtered_account_summary_items(self, client_id, start_date, end_date):
        return AccountSummaryItem.objects.filter(
            client__id=client_id, date__date__gte=start_date, date__date__lte=end_date
        ).order_by("date")

    def list(self, request):
        try:
            client_id, start_date, end_date = self.get_params_from_request(request)
        except ParseError:
            return HttpResponse(status=400)

        self.queryset = self.get_filtered_account_summary_items(
            client_id, start_date, end_date
        )
        return super().list(request)

    @action(detail=False, methods=["get"])
    def download_pdf(self, request):
        try:
            client_id, start_date, end_date = self.get_params_from_request(request)
        except ParseError:
            return HttpResponse(status=400)

        account_summary_items = self.get_filtered_account_summary_items(
            client_id, start_date, end_date
        )

        parsed_account_summary_items = []
        total = 0
        for item in account_summary_items:
            parsed_item = {
                "date": item.date,
                "description": item.description,
            }
            if item.type == DEBE:
                parsed_item["debe"] = item.amount
                total += item.amount
            else:  # item.type == HABER
                parsed_item["haber"] = item.amount
                total -= item.amount
            parsed_item["total"] = total
            parsed_account_summary_items.append(parsed_item)
        parsed_account_summary_items.append({"total": total})

        context = {
            "client": Cliente.objects.get(id=client_id),
            "account_summary_items": parsed_account_summary_items,
        }
        pdf = render_to_pdf("pdf/account_summary_pdf.html", context)
        if not pdf:
            return HttpResponse(status=500)
        response = HttpResponse(pdf, content_type="application/pdf")
        filename = f"resumen_de_cuenta_cliente_{client_id}.pdf"
        content = f"inline; filename='{filename}'"
        download = request.GET.get("download")
        if download:
            content = f"attachment; filename={filename}"
        response["Content-Disposition"] = content
        return response
