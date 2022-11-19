from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from lubricentro_myc.models import ProductPriceHistory
from lubricentro_myc.models.product import Producto
from lubricentro_myc.serializers.product import ProductoSerializer
from lubricentro_myc.views.pagination import CustomPageNumberPagination
from rest_framework import viewsets
from rest_framework.decorators import action


class ProductoViewSet(viewsets.ModelViewSet, CustomPageNumberPagination):
    queryset = Producto.objects.all().order_by("codigo_en_pantalla")
    serializer_class = ProductoSerializer
    pagination_class = CustomPageNumberPagination

    def list(self, request):
        detalle = request.GET.get("detalle", None)
        categoria = request.GET.get("categoria", None)
        query = request.GET.get("query", None)
        if detalle:
            self.queryset = Producto.objects.filter(
                detalle__icontains=detalle
            ).order_by("codigo_en_pantalla")
        elif categoria:
            self.queryset = Producto.objects.filter(
                categoria__iexact=categoria
            ).order_by("codigo_en_pantalla")
        elif query:
            if query.isnumeric():
                self.queryset = Producto.objects.filter(
                    codigo_en_pantalla__gte=query
                ).order_by("codigo_en_pantalla")
            else:
                self.queryset = Producto.objects.filter(
                    Q(codigo_en_pantalla__contains=query)
                    | Q(detalle__icontains=query)
                    | Q(categoria__icontains=query)
                ).order_by("codigo_en_pantalla")
        return super().list(request)

    @action(detail=False, methods=["post"])
    def aumento_masivo_precio_costo(self, request):
        producto_ids = request.data.get("productos")
        porcentaje_aumento = request.data.get("porcentaje_aumento")
        if not producto_ids or not porcentaje_aumento:
            return HttpResponse(status=400)
        aumento = 1 + int(porcentaje_aumento) / 100
        updated_products = 0
        for producto_id in producto_ids:
            try:
                p = Producto.objects.get(codigo=producto_id)
                p.precio_costo = p.precio_costo * aumento
                p.save()
                updated_products += 1
            except Producto.DoesNotExist:
                pass
        return JsonResponse(
            data={
                "resultado": f"{updated_products} producto/s actualizado/s satisfactoriamente."
            }
        )

    @action(detail=True, methods=["get"])
    def historial_precios(self, request, pk=None):
        try:
            Producto.objects.get(codigo=pk)
        except Producto.DoesNotExist:
            return HttpResponse(status=404)
        prices_history = ProductPriceHistory.objects.filter(product__codigo=pk)
        return JsonResponse(
            data={
                "prices": [
                    {
                        "old_price": round(price.old_price, 2),
                        "new_price": round(price.new_price, 2),
                        "date": price.timestamp,
                    }
                    for price in prices_history
                ]
            }
        )

    @action(detail=False, methods=["get"])
    def codigos_disponibles(self, request):
        start = int(request.GET.get("start", 1))
        amount = int(request.GET.get("amount", 10))
        codes_in_used = Producto.objects.all().values_list(
            "codigo_en_pantalla", flat=True
        )
        available_codes = list(set(list(range(start, 100001))) - set(codes_in_used))
        closest_code = min(available_codes, key=lambda x: abs(x - start))
        closest_code_index = available_codes.index(closest_code)
        return JsonResponse(
            data={
                "available_codes": available_codes[
                    closest_code_index : closest_code_index + amount
                ]
            }
        )
