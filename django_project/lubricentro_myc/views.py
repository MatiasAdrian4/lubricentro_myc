from django.http import Http404
from django.views.generic.list import ListView
from rest_framework import viewsets

from .models import Cliente, Producto
from .serializers import ClienteSerializer, ProductoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoListView(ListView):
    model = Producto
    template_name = 'productos.html'

    def get_queryset(self):
        args = self.request.GET
        if 'codigo' in args.keys():
            queryset = []
            try:
                producto = Producto.objects.get(codigo=args['codigo'])
            except Producto.DoesNotExist:
                print('no existe')
                return []
            queryset.append(producto)
            return queryset
        elif 'detalle' in args.keys():
           return Producto.objects.filter(detalle__contains=args['detalle'])
        elif 'categoria' in args.keys():
            return Producto.objects.filter(categoria=args['categoria'])
        else:
            return Producto.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductoListView,self).get_context_data(**kwargs)
        context['url'] = self.request.build_absolute_uri(self.request.path)
        return context
