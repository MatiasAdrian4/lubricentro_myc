import calendar
from calendar import monthrange

from django.db.models import Q, Sum
from django.http import HttpResponse, JsonResponse
from lubricentro_myc.models.client import Cliente
from lubricentro_myc.models.product import Producto
from lubricentro_myc.models.sale import Venta
from lubricentro_myc.serializers.sale import VentaSerializer, VentasSerializer
from lubricentro_myc.views.pagination import CustomPageNumberPagination
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class VentaViewSet(viewsets.ModelViewSet, CustomPageNumberPagination):
    queryset = Venta.objects.all().order_by("id")
    serializer_class = VentaSerializer
    pagination_class = CustomPageNumberPagination

    def list(self, request):
        dia = request.GET.get("dia")
        mes = request.GET.get("mes")
        anio = request.GET.get("anio")
        if dia or mes or anio:
            filters = Q()
            if anio:
                filters &= Q(fecha__year=int(anio))
            else:
                return HttpResponse(status=400)
            if mes:
                filters &= Q(fecha__month=int(mes))
            elif dia:
                return HttpResponse(status=400)
            if dia:
                filters &= Q(fecha__day=int(dia))
            if filters:
                self.queryset = Venta.objects.filter(filters).order_by("fecha")
        return super().list(request)

    def store_sale(self, venta, update_stock):
        product = Producto.objects.get(codigo=venta["producto"]["codigo"])
        Venta.objects.create(
            producto=product,
            cantidad=venta["cantidad"],
            precio=venta["precio"],
        )
        if update_stock:
            product.stock -= venta["cantidad"]
            product.save()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_stock = True if request.GET.get("update_stock") == "true" else False
        self.store_sale(serializer.data, update_stock)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def bulk(self, request):
        serializer = VentasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_stock = True if request.GET.get("update_stock") == "true" else False
        for venta in serializer.data["ventas"]:
            self.store_sale(venta, update_stock)
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

    @action(detail=False, methods=["get"])
    def historial_deudores(self, request):
        total_debt = 0
        clients = []
        for client in Cliente.objects.all():
            client_debt = client.deuda_actual
            if client_debt > 0:
                total_debt += client_debt
                clients.append(
                    {
                        "id": client.id,
                        "nombre": client.nombre,
                        "deuda_actual": client_debt,
                    }
                )
        return JsonResponse(
            data={
                "clientes": sorted(
                    clients, key=lambda d: d["deuda_actual"], reverse=True
                ),
                "deuda_total": total_debt,
            }
        )
