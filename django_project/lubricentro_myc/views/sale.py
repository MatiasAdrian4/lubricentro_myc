from calendar import monthrange

from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from lubricentro_myc.models import Venta, Producto
from lubricentro_myc.serializers.sale import VentaSerializer


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

    @action(detail=False, methods=['post'])
    def guardar_venta(self, request):
        ventas = self.request.data['ventas']
        for venta in ventas:
            producto = Producto.objects.get(codigo=venta['producto'])
            nueva_venta = Venta(
                producto=producto, cantidad=venta['cantidad'], precio=venta['precio'])
            nueva_venta.save()
        return HttpResponse(status=200)


    @action(detail=False, methods=['post'])
    def guardar_venta_y_actualizar_stock(self, request):
        ventas = self.request.data['ventas']
        for venta in ventas:
            producto = Producto.objects.get(codigo=venta['producto'])
            producto.stock -= float(venta['cantidad'])
            producto.save()
            nueva_venta = Venta(
                producto=producto, cantidad=venta['cantidad'], precio=venta['precio'])
            nueva_venta.save()
        return HttpResponse(status=200)

    @action(detail=False, methods=['get'])
    def ventas_por_mes_anio(self, request):
        search_type = request.GET.get('search_type', '')
        if (search_type == "year"):
            year = request.GET.get('year', '')
            labels = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            data = []
            for i in range(13):
                ventas = Venta.objects.filter(
                    fecha__month=int(i+1),
                    fecha__year=int(year)
                )
                suma_ventas = ventas.aggregate(Sum('precio'))['precio__sum']
                if suma_ventas is not None:
                    data.append(round(suma_ventas, 2))
                else:
                    data.append(0)
        elif (search_type == "month"):
            year = request.GET.get('year', '')
            month = request.GET.get('month', '')
            days = monthrange(int(year), int(month))
            labels = []
            data = []
            for i in range(days[1]):
                labels.append(i+1)
                ventas = Venta.objects.filter(
                    fecha__day=int(i+1),
                    fecha__month=int(month),
                    fecha__year=int(year)
                )
                suma_ventas = ventas.aggregate(Sum('precio'))['precio__sum']
                if suma_ventas is not None:
                    data.append(round(suma_ventas, 2))
                else:
                    data.append(0)
        return JsonResponse(
            data={
                'labels': labels,
                'data': data
            })