from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.template.loader import get_template
from rest_framework import viewsets
from rest_framework.decorators import action

from .models import Cliente, Producto, Remito, ElementoRemito
from .serializers import ClienteSerializer, ProductoSerializer, RemitoSerializer, ElementoRemitoSerializer
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

def generar_stock_pdf(request, *args, **kwargs):
    categoria = request.GET['categoria']
    if categoria is not None:
        productos = Producto.objects.filter(categoria=categoria)
    else:
        productos = Producto.objects.none()

    template = get_template('stock.html')
    context = {
        "categoria" : categoria,
        "productos" : productos
    }
    html = template.render(context)
    pdf = render_to_pdf('stock.html', context)
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
    template = get_template('remito.html')
    context = {
    }
    html = template.render(context)
    pdf = render_to_pdf('remito.html', context)
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
    
