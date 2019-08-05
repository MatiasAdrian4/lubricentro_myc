from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.template.loader import get_template
from rest_framework import viewsets

from .models import Cliente, Producto
from .serializers import ClienteSerializer, ProductoSerializer
from .utils import render_to_pdf

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class InventarioView(ListView):
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
        context = super(InventarioView,self).get_context_data(**kwargs)
        context['url'] = self.request.build_absolute_uri(self.request.path)
        categorias = Producto.objects.order_by().values('categoria').distinct()
        context['categorias'] = categorias
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
