from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from lubricentro_myc.models import Producto, Cliente, Remito, ElementoRemito, Venta


def ventas(request):
    host = request.scheme + "://" + request.META['HTTP_HOST']
    context = {'host': host}
    return render(request, 'ventas.html', context=context)


def remitos_facturacion(request):
    context = {}
    return render(request, 'remitos_facturacion.html', context=context)


class ImpresionStock(TemplateView):
    template_name = "impresion_stock.html"

    def get_context_data(self, **kwargs):
        context = super(ImpresionStock, self).get_context_data(**kwargs)
        categorias = Producto.objects.order_by().values('categoria').distinct()
        context['categorias'] = categorias
        return context


class CSV(TemplateView):
    template_name = "csv.html"


class Inventario(ListView):
    model = Producto
    template_name = 'inventario.html'

    def get_queryset(self):
        args = self.request.GET
        queryset = []
        if 'codigo' in args.keys():
            if args['codigo'] == 'undefined':
                return []
            else:
                try:
                    producto = Producto.objects.get(codigo=args['codigo'])
                except Producto.DoesNotExist:
                    return []
            queryset.append(producto)
            return queryset
        elif 'detalle' in args.keys():
            if len(args['detalle'].strip()) == 0:
                return []
            return Producto.objects.filter(detalle__icontains=args['detalle']).order_by('codigo')
        elif 'categoria' in args.keys():
            return Producto.objects.filter(categoria=args['categoria']).order_by('codigo')
        else:
            return queryset

    def get_context_data(self, **kwargs):
        context = super(Inventario, self).get_context_data(**kwargs)
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
            return Cliente.objects.filter(nombre__icontains=args['nombre']).order_by('id')
        else:
            return Cliente.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super(ListadoClientes, self).get_context_data(**kwargs)
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
            return Remito.objects.filter(cliente__nombre__icontains=args['cliente']).order_by('-codigo')
        else:
            return Remito.objects.all().order_by('-codigo')

    def get_context_data(self, **kwargs):
        context = super(Remitos, self).get_context_data(**kwargs)
        context['host'] = self.request.scheme + \
            "://" + self.request.META['HTTP_HOST']
        context['url'] = self.request.build_absolute_uri(self.request.path)
        return context


class RemitosEdicion(ListView):
    model = Producto
    template_name = 'remitos_edicion.html'

    def get_queryset(self):
        args = self.request.GET
        queryset = []
        if 'codigo' in args.keys():
            if args['codigo'] == 'undefined':
                return []
            else:
                try:
                    remito = Remito.objects.get(codigo=args['codigo'])
                except Producto.DoesNotExist:
                    return []
            for elemento_remito in ElementoRemito.objects.filter(remito_id=remito.codigo):
                elem_remito = {}
                if not elemento_remito.pagado:
                    elem_remito['id'] = elemento_remito.id
                    elem_remito['producto_id'] = elemento_remito.producto.codigo
                    elem_remito['producto_detalle'] = elemento_remito.producto.detalle
                    elem_remito['cantidad'] = elemento_remito.cantidad
                    queryset.append(elem_remito)
            return queryset
        else:
            return queryset

    def get_context_data(self, **kwargs):
        context = super(RemitosEdicion, self).get_context_data(**kwargs)
        args = self.request.GET
        if 'codigo' in args.keys():
            context['nro_remito'] = args['codigo']
        context['url'] = self.request.build_absolute_uri(self.request.path)
        return context


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
            ).order_by('fecha')
        elif 'mes' in args.keys():
            return Venta.objects.filter(
                fecha__month=int(args['mes'][0:2]),
                fecha__year=int(args['mes'][3:7])
            ).order_by('fecha')
        else:
            return []

    def get_context_data(self, **kwargs):
        context = super(HistorialVentas, self).get_context_data(**kwargs)
        ventas = self.get_queryset()
        total = 0
        for venta in ventas:
            total += venta.precio
        context['total'] = total
        return context