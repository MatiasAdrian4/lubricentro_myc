from django.db.models import Max
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from lubricentro_myc.models import Producto, Venta, ElementoRemito
from lubricentro_myc.serializers.product import ProductoSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def create(self, request):
        codigo = request.data['codigo']
        if codigo != "":
            try:
                Producto.objects.get(codigo=codigo)
                return HttpResponse("Código en uso por otro producto", status=500)
            except Producto.DoesNotExist:
                pass
        else:
            max_codigo = Producto.objects.aggregate(Max('codigo'))
            codigo = max_codigo['codigo__max'] + 1
        request.data['codigo'] = codigo
        return super().create(request)

    @action(detail=False, methods=['get'])
    def buscar_por_detalle(self, request):
        resultado = []
        detalle = request.GET.get('detalle', '')
        if detalle == '':
            return JsonResponse(data={'productos': resultado})
        for producto in Producto.objects.filter(detalle__icontains=detalle).values():
            resultado.append({
                "codigo": producto['codigo'],
                "detalle": producto['detalle'],
                "precio_costo": producto['precio_costo']
            })
        return JsonResponse(data={'productos': resultado})

    @action(detail=False, methods=['get'])
    def buscar_por_categoria(self, request):
        resultado = []
        categoria = request.GET.get('categoria', '')
        if categoria == '':
            return JsonResponse(data={'productos': resultado})
        for producto in Producto.objects.filter(categoria=categoria).values():
            resultado.append({
                "codigo": producto['codigo'],
                "detalle": producto['detalle'],
                "precio_costo": producto['precio_costo']
            })
        return JsonResponse(data={'productos': resultado})

    # TODO:
    #   Este approach fue para salir del paso. No es una buena solución actualizar el id del producto y sus referencias.
    #   Se tendria que agregar otro tipo de pk al modelo Producto (id_hash por ejemplo).
    #   Se deberian actualizar todas las referencias actuales al campo código para que apunten al nuevo id.
    #   Se deberian actualizar todos los métodos que hacen uso del código del Producto como fk, para que usen ahora el nuevo id.

    @action(detail=False, methods=['post'])
    def custom_update(self, request):
        codigo_real = request.data['codigo_real']
        producto = request.data['producto']

        if(codigo_real != producto['codigo']):
            # Grabo el nuevo elemento, actualizo las referencias y elimino el elemento anterior
            try:
                Producto.objects.get(codigo=producto['codigo'])
                return HttpResponse("Código en uso por otro producto", status=500)
            except Producto.DoesNotExist:
                nuevo_producto = Producto.objects.create(
                    codigo=producto['codigo'],
                    detalle=producto['detalle'],
                    stock=producto['stock'],
                    precio_costo=producto['precio_costo'],
                    desc1=producto['desc1'],
                    desc2=producto['desc2'],
                    desc3=producto['desc3'],
                    desc4=producto['desc4'],
                    flete=producto['flete'],
                    ganancia=producto['ganancia'],
                    iva=producto['iva'],
                    agregado_cta_cte=producto['agregado_cta_cte'],
                    categoria=producto['categoria']
                )
                nuevo_producto.save()

                ventas_asociadas = Venta.objects.filter(producto__codigo=codigo_real)
                ventas_asociadas.update(producto=nuevo_producto)

                elementos_remito_asociados = ElementoRemito.objects.filter(producto__codigo=codigo_real)
                elementos_remito_asociados.update(producto=nuevo_producto)

                producto_actual = Producto.objects.get(codigo=codigo_real)
                producto_actual.delete()
        else:
            producto_actual = Producto.objects.get(codigo=codigo_real)
            producto_actual.detalle = producto['detalle']
            producto_actual.stock = float(producto['stock'])
            producto_actual.precio_costo = producto['precio_costo']
            producto_actual.desc1 = producto['desc1']
            producto_actual.desc2 = producto['desc2']
            producto_actual.desc3 = producto['desc3']
            producto_actual.desc4 = producto['desc4']
            producto_actual.flete = producto['flete']
            producto_actual.ganancia = producto['ganancia']
            producto_actual.iva = producto['iva']
            producto_actual.agregado_cta_cte = producto['agregado_cta_cte']
            producto_actual.categoria = producto['categoria']
            producto_actual.save()

        return HttpResponse(status=200)

    @action(detail=False, methods=['post'])
    def aumento_masivo_precio_costo(self, request):
        productos = request.data['productos']
        porcentaje_aumento = request.data['porcentaje_aumento']
        aumento = 1 + int(porcentaje_aumento)/100
        for producto in productos:
            p = Producto.objects.get(codigo=producto)
            p.precio_costo = p.precio_costo * aumento
            p.save()
        resultado = str(len(productos)) + " producto/s actualizado/s satisfactoriamente."
        return JsonResponse(data={'resultado': resultado})

    # TODO: agregar aca un limite desde ui
    @action(detail=False, methods=['get'])
    def buscar_codigo_libre(self, request):
        desde = int(request.GET.get('desde', ''))
        hasta = desde + 10000
        for i in range(desde, hasta):
            try:
                Producto.objects.get(codigo=i)
            except Producto.DoesNotExist:
                return JsonResponse(data={'codigo': i})
        return JsonResponse(data={'codigo': None})