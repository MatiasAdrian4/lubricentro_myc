import calendar
from calendar import monthrange

from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from lubricentro_myc.models.sale import Venta
from lubricentro_myc.serializers.sale import VentaSerializer, VentasSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all().order_by("id")
    serializer_class = VentaSerializer

    def store_sale(self, request, update_stock=False):
        serializer = VentasSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        ventas = serializer.validated_data.get("ventas")
        for venta in ventas:
            nueva_venta = Venta(
                producto=venta.get("producto"),
                cantidad=venta.get("cantidad"),
                precio=venta.get("precio"),
            )
            nueva_venta.save()
            if update_stock:
                producto = venta.get("producto")
                producto.stock -= float(venta.get("cantidad"))
                producto.save()
        return HttpResponse(status=200)

    @action(detail=False, methods=["post"])
    def guardar_venta(self, request):
        return self.store_sale(request)

    @action(detail=False, methods=["post"])
    def guardar_venta_y_actualizar_stock(self, request):
        return self.store_sale(request, True)

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
