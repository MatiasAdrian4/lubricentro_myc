from django.http import HttpResponse
from lubricentro_myc.models import (
    Cliente,
    ElementoRemito,
    Producto,
    ProductPriceHistory,
    Remito,
    Venta,
)


def reset(request):
    # This endpoint is intended to clean up the database after running E2E tests.

    ElementoRemito.objects.all().delete()
    Remito.objects.all().delete()
    Venta.objects.all().delete()
    Cliente.objects.all().delete()
    ProductPriceHistory.objects.all().delete()
    Producto.objects.all().delete()

    return HttpResponse(status=200)
