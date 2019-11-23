from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.template.loader import get_template
from rest_framework import viewsets
from rest_framework.decorators import action
from datetime import datetime

from .models import Cliente, Producto, Remito, ElementoRemito, Venta
from .serializers import ClienteSerializer, ProductoSerializer, RemitoSerializer, ElementoRemitoSerializer, VentaSerializer
from .utils import render_to_pdf

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    @action(detail=False, methods=['get'])
    def buscar(self, request):
        resultado = []
        nombre = request.GET.get('nombre', '')
        if nombre == '':
            return JsonResponse(data={'clientes': resultado})
        for cliente in Cliente.objects.filter(nombre__icontains=nombre).values():
            resultado.append({
                "codigo": cliente['id'],
                "nombre": cliente['nombre']
            })
        return JsonResponse(data={'clientes': resultado})

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    @action(detail=False, methods=['get'])
    def buscar(self, request):
        resultado = []
        detalle = request.GET.get('detalle', '')
        if detalle == '':
            return JsonResponse(data={'productos': resultado})
        for producto in Producto.objects.filter(detalle__icontains=detalle).values():
            resultado.append({
                "codigo": producto['codigo'],
                "detalle": producto['detalle']
            })
        return JsonResponse(data={'productos': resultado})

class RemitoViewSet(viewsets.ModelViewSet):
    queryset = Remito.objects.all()
    serializer_class = RemitoSerializer

class ElementoRemitoViewSet(viewsets.ModelViewSet):
    queryset = ElementoRemito.objects.all()
    serializer_class = ElementoRemitoSerializer

    @action(detail=False, methods=['get'])
    def buscar(self, request):
        lista_productos = {}
        codigo = request.GET.get('codigo', '')
        elementos_remito = ElementoRemito.objects.filter(remito__cliente=codigo, pagado=False)
        resultado = []
        for elem in elementos_remito:
            prod = Producto.objects.get(codigo=elem.producto_id)
            resultado.append({
                "elem_remito": elem.id,
                "codigo": prod.codigo,
                "detalle": prod.detalle,
                "precio_cta_cte" : prod.precio_venta_cta_cte,
                "cantidad": elem.cantidad
            })
        return JsonResponse(data={'elementos_remito': resultado})

    @action(methods=['post'], detail=False)
    def marcar_pagado(self, request):
        elem_remito = ElementoRemito.objects.get(id=self.request.data['id'])
        elem_remito.pagado = True
        elem_remito.save()
        return HttpResponse(status=200)

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

def ventas(request):
    host = request.scheme + "://" + request.META['HTTP_HOST']
    context = {'host': host}
    return render(request, 'ventas.html', context=context)

class Inventario(ListView):
    model = Producto
    template_name = 'inventario.html'

    def get_queryset(self):
        args = self.request.GET
        queryset = []
        if 'codigo' in args.keys():
            try:
                producto = Producto.objects.get(codigo=args['codigo'])
            except Producto.DoesNotExist:
                return []
            queryset.append(producto)
            return queryset
        elif 'detalle' in args.keys():
            if len(args['detalle'].strip()) == 0:
                return []
            return Producto.objects.filter(detalle__icontains=args['detalle'])
        elif 'categoria' in args.keys():
            return Producto.objects.filter(categoria=args['categoria'])
        else:
            return queryset

    def get_context_data(self, **kwargs):
        context = super(Inventario,self).get_context_data(**kwargs)
        context['url'] = self.request.build_absolute_uri(self.request.path)
        categorias = Producto.objects.order_by().values('categoria').distinct()
        context['categorias'] = categorias
        return context

class ListadoClientes(ListView):
    model = Cliente
    template_name = 'listado_clientes.html'

    def get_queryset(self):
        args = self.request.GET
        queryset = []
        if 'codigo' in args.keys():
            try:
                cliente = Cliente.objects.get(id=args['codigo'])
            except Cliente.DoesNotExist:
                return []
            queryset.append(cliente)
            return queryset
        elif 'nombre' in args.keys():
            if len(args['nombre'].strip()) == 0:
                return []
            return Cliente.objects.filter(nombre__icontains=args['nombre'])
        else:
            return Cliente.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ListadoClientes,self).get_context_data(**kwargs)
        context['url'] = self.request.build_absolute_uri(self.request.path)
        return context

class Remitos(ListView):
    model = Remito
    template_name = "remitos.html"

    def get_queryset(self):
        args = self.request.GET
        queryset = []
        if 'codigo' in args.keys():
            try:
                remito = Remito.objects.get(codigo=args['codigo'])
            except Remito.DoesNotExist:
                return []
            queryset.append(remito)
            return queryset
        elif 'cliente' in args.keys():
            if len(args['cliente'].strip()) == 0:
                return []
            return Remito.objects.filter(cliente__nombre__icontains=args['cliente'])
        else:
            return Remito.objects.all()

    def get_context_data(self, **kwargs):
        context = super(Remitos,self).get_context_data(**kwargs)
        context['host'] = self.request.scheme + "://" + self.request.META['HTTP_HOST']
        context['url'] = self.request.build_absolute_uri(self.request.path)
        return context

def remitos_facturacion(request):
    context = {}
    return render(request, 'remitos_facturacion.html', context=context)

def generar_stock_pdf(request, *args, **kwargs):
    template = get_template('stock_pdf.html')

    categoria = request.GET['categoria']
    if categoria is not None:
        productos = Producto.objects.filter(categoria=categoria)
    else:
        productos = Producto.objects.none()
    context = {
        "categoria" : categoria,
        "productos" : productos
    }
    html = template.render(context)
    pdf = render_to_pdf('stock_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'stock_%s.pdf' %(categoria)
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

def generar_remito_pdf(request, *args, **kwargs):
    template = get_template('remito_pdf.html')

    remito = Remito.objects.get(codigo=request.GET['cod_remito'])
    elementos_remito = []
    for elemento in ElementoRemito.objects.filter(remito=remito):
        producto = Producto.objects.get(codigo = elemento.producto_id)
        elemento_remito = {}
        elemento_remito['codigo'] = producto.codigo
        elemento_remito['detalle'] = producto.detalle
        elemento_remito['cantidad'] = elemento.cantidad
        elementos_remito.append(elemento_remito)
    context = {
        "remito" : remito,
        "cliente" : Cliente.objects.get(id=remito.cliente_id),
        "elementos_remito" : elementos_remito
    }
    html = template.render(context)
    pdf = render_to_pdf('remito_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'remito_%s.pdf' %('editar_aca')
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
    
class HistorialVentas(ListView):
    model = Venta
    template_name = "ventas_historial.html"

    def get_queryset(self):
        args = self.request.GET
        if 'fecha' in args.keys():
            return Venta.objects.filter(
                fecha__day=int(args['fecha'][0:2]),
                fecha__month=int(args['fecha'][3:5]),
                fecha__year=int(args['fecha'][6:10])
            )
        elif 'mes' in args.keys():
            return Venta.objects.filter(
                fecha__month=int(args['mes'][0:2]),
                fecha__year=int(args['mes'][3:7])
            )
        else:
            return Venta.objects.all()

    def get_context_data(self, **kwargs):
        context = super(HistorialVentas,self).get_context_data(**kwargs)
        return context