import calendar
from calendar import monthrange

from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from lubricentro_myc.models.product import Producto
from lubricentro_myc.models.sale import Venta
from lubricentro_myc.serializers.sale import VentaSerializer, VentasSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all().order_by("id")
    serializer_class = VentaSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_stock = True if request.GET.get("update_stock") == "true" else False
        product = Producto.objects.get(codigo=serializer.data["producto"])
        Venta.objects.create(
            producto=product,
            cantidad=serializer.data["cantidad"],
            precio=serializer.data["precio"],
        )
        if update_stock:
            product.stock -= serializer.data["cantidad"]
            product.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def ventas_por_anio(self, request):
        year = request.GET.get("year")
        if not year:
            return HttpResponse(status=400)
        data = []
        for i in range(12):
            ventas = Venta.objects.filter(
                fecha__month=int(i + 1), fecha__year=int(year)
            )
            suma_ventas = ventas.aggregate(Sum("precio"))["precio__sum"]
            data.append(round(suma_ventas, 2) if suma_ventas else 0)
        return JsonResponse(data={"sales_per_year": data})

    @action(detail=False, methods=["get"])
    def ventas_por_mes(self, request):
        year = request.GET.get("year")
        month = request.GET.get("month")
        if not year or not month:
            return HttpResponse(status=400)
        try:
            days = monthrange(int(year), int(month))
        except calendar.IllegalMonthError:
            return HttpResponse(status=400)
        data = []
        for i in range(days[1]):
            ventas = Venta.objects.filter(
                fecha__day=int(i + 1),
                fecha__month=int(month),
                fecha__year=int(year),
            )
            suma_ventas = ventas.aggregate(Sum("precio"))["precio__sum"]
            data.append(round(suma_ventas, 2) if suma_ventas else 0)
        return JsonResponse(data={"sales_per_month": data})
