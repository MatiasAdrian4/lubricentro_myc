import csv
import json
import os
import traceback
import zipfile

from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from rest_framework.decorators import permission_classes, api_view

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
from lubricentro_myc.permissions import IsSuperAdmin
from lubricentro_myc.serializers.activity import ActivitySerializer
from lubricentro_myc.utils import log_activity


@api_view(["GET"])
@permission_classes([IsSuperAdmin])
def activities_list(request):
    type = request.query_params.get("type")
    activities = Activity.objects.filter(type=type) if type else Activity.objects.all()
    serializer = ActivitySerializer(activities, many=True)
    return JsonResponse(data={"activities": serializer.data})


@api_view(["GET"])
@permission_classes([IsSuperAdmin])
def activity_details(_, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
    except Activity.DoesNotExist:
        return HttpResponse(status=404)

    serializer = ActivitySerializer(activity)
    return JsonResponse(data=serializer.data)


@api_view(["GET"])
@permission_classes([IsSuperAdmin])
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

            for model_name, queryset in models_to_export:
                f = open(f"{model_name}.csv", "w")
                writer = csv.writer(f, delimiter="|")
                for obj in queryset:
                    writer.writerow(obj.data)

                zipf.write(f"{model_name}.csv", arcname=f"{model_name}.csv")
                os.remove(f"{model_name}.csv")

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
