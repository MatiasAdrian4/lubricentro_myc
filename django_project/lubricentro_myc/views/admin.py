import csv
import json
import os
import traceback
import zipfile

from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from lubricentro_myc.models import (
    Activity,
    Producto,
    ProductPriceHistory,
    Cliente,
    Venta,
    Remito,
    ElementoRemito,
)
from lubricentro_myc.models.activity import EXCEPTION, INFO
from lubricentro_myc.serializers.activity import ActivitySerializer
from lubricentro_myc.utils import log_activity


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def activities_list(_):
    serializer = ActivitySerializer(Activity.objects.all(), many=True)
    return JsonResponse(data={"activities": serializer.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def activity_details(_, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
    except Activity.DoesNotExist:
        return HttpResponse(status=404)

    serializer = ActivitySerializer(activity)
    return JsonResponse(data=serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_models_backup(request):
    start_activity = log_activity(
        request, INFO, "Models Backup Export", json.dumps(request.data)
    )
    try:
        response = HttpResponse(content_type="application/zip")
        response["Content-Disposition"] = (
            f'attachment; filename="models_backup_{timezone.now()}.zip"'
        )

        with zipfile.ZipFile(response, "w") as zipf:
            models_to_export = [
                ("products", Producto.objects.all()),
                ("product_prices_history", ProductPriceHistory.objects.all()),
                ("clients", Cliente.objects.all()),
                ("sales", Venta.objects.all()),
                ("invoices", Remito.objects.all()),
                ("invoice_items", ElementoRemito.objects.all()),
            ]

            for filename, queryset in models_to_export:
                f = open(f"{filename}.csv", "w")
                writer = csv.writer(f, delimiter="|")
                for obj in queryset:
                    writer.writerow(obj.data)

                zipf.write(f"{filename}.csv", arcname=f"{filename}.csv")
                os.remove(f"{filename}.csv")

        return response
    except:
        log_activity(
            request,
            EXCEPTION,
            "Models Backup Export Failed",
            traceback.format_exc(),
            start_activity,
        )
        return HttpResponse(status=500)
