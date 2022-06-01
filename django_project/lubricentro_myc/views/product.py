from django.http import HttpResponse, JsonResponse
from lubricentro_myc.models.product import Producto
from lubricentro_myc.serializers.product import ProductoSerializer
from rest_framework import viewsets
from rest_framework.decorators import action


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('codigo')
    serializer_class = ProductoSerializer

    def list(self, request):
        detalle = request.GET.get("detalle", None)
        categoria = request.GET.get("categoria", None)
        if detalle:
            self.queryset = Producto.objects.filter(detalle__icontains=detalle).order_by('codigo')
        elif categoria:
            self.queryset = Producto.objects.filter(categoria__iexact=categoria).order_by('codigo')
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
