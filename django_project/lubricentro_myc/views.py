import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.template.loader import get_template
from rest_framework import viewsets
from rest_framework.decorators import action
from calendar import monthrange
from django.db.models import Sum, Max
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import csv
import io

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
            producto_actual.stock = int(producto['stock'])
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


class RemitoViewSet(viewsets.ModelViewSet):
    queryset = Remito.objects.all()
    serializer_class = RemitoSerializer


class ElementoRemitoViewSet(viewsets.ModelViewSet):
    queryset = ElementoRemito.objects.all()
    serializer_class = ElementoRemitoSerializer

    @action(detail=False, methods=['get'])
    def buscar(self, request):
        codigo = request.GET.get('codigo', '')
        elementos_remito = ElementoRemito.objects.filter(
            remito__cliente=codigo, pagado=False)
        resultado = []
        for elem in elementos_remito:
            prod = Producto.objects.get(codigo=elem.producto_id)
            resultado.append({
                "elem_remito": elem.id,
                "remito": elem.remito.codigo,
                "codigo": prod.codigo,
                "detalle": prod.detalle,
                "precio_cta_cte": prod.precio_venta_cta_cte,
                "cantidad": elem.cantidad
            })
        return JsonResponse(data={'elementos_remito': resultado})

    @action(methods=['post'], detail=False)
    def marcar_pagado(self, request):
        elems = self.request.data['elementos']
        for elem in elems:
            elem_remito = ElementoRemito.objects.get(id=elem['id'])
            elem_remito.pagado = True
            elem_remito.save()
        return HttpResponse(status=200)

    @action(methods=['post'], detail=False)
    def guardar_elementos(self, request):
        elems = self.request.data['elementos']
        for elem in elems:
            new_elem = ElementoRemito(
                remito=Remito.objects.get(codigo=elem['remito']), producto=Producto.objects.get(codigo=elem['producto']), cantidad=elem['cantidad'], pagado=False)
            new_elem.save()
        return HttpResponse(status=200)


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
            return Producto.objects.filter(detalle__icontains=args['detalle'])
        elif 'categoria' in args.keys():
            return Producto.objects.filter(categoria=args['categoria'])
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
            return Cliente.objects.filter(nombre__icontains=args['nombre'])
        else:
            return Cliente.objects.all()

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


def remitos_facturacion(request):
    context = {}
    return render(request, 'remitos_facturacion.html', context=context)


def generar_stock_pdf(request, *args, **kwargs):
    template = get_template('pdf/stock_pdf.html')

    categoria = request.GET['categoria']
    if categoria is not None:
        productos = Producto.objects.filter(categoria__iexact=categoria)
    else:
        productos = Producto.objects.none()
    context = {
        "categoria": categoria,
        "productos": productos
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/stock_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'stock_%s.pdf' % (categoria)
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename=%s" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


def generar_remito_pdf(request, *args, **kwargs):
    template = get_template('pdf/remito_pdf.html')

    remito = Remito.objects.get(codigo=request.GET['cod_remito'])
    elementos_remito = []
    for elemento in ElementoRemito.objects.filter(remito=remito):
        producto = Producto.objects.get(codigo=elemento.producto_id)
        elemento_remito = {}
        elemento_remito['codigo'] = producto.codigo
        elemento_remito['detalle'] = producto.detalle
        elemento_remito['cantidad'] = elemento.cantidad
        elementos_remito.append(elemento_remito)
    context = {
        "remito": remito,
        "cliente": Cliente.objects.get(id=remito.cliente_id),
        "elementos_remito": elementos_remito
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/remito_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'remito_%s.pdf' % ('editar_aca')
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename=%s" % (filename)
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
            ).order_by('fecha')
        elif 'mes' in args.keys():
            return Venta.objects.filter(
                fecha__month=int(args['mes'][0:2]),
                fecha__year=int(args['mes'][3:7])
            ).order_by('fecha')
        else:
            return Venta.objects.all().order_by('fecha')

    def get_context_data(self, **kwargs):
        context = super(HistorialVentas, self).get_context_data(**kwargs)
        ventas = self.get_queryset()
        total = 0
        for venta in ventas:
            total += venta.precio
        context['total'] = total
        return context


@require_http_methods(["POST"])
def crear_usuario(request):
    data = json.loads(request.body.decode('utf-8'))
    user = User.objects.create_user(
        username=data['nombre'],
        password=data['password'],
        email=data['email'],
    )
    user.save()
    return HttpResponse(status=200)


class CSV(TemplateView):
    template_name = "csv.html"


def importar_csv(request):

    model = request.POST.get('model', '')
    if model == '':
        return redirect('/lubricentro_myc/acciones_csv')

    if model == 'clientes':
        queryset = Cliente.objects.all()
        if len(queryset) > 0:
            print("ya hay " + str(len(queryset)) +
                  " clientes en la base de datos")
        else:
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                print(column)
                Cliente.objects.create(
                    id=column[0],
                    nombre=column[1],
                    direccion=column[2],
                    localidad=column[3],
                    codigo_postal=column[4],
                    telefono=column[5],
                    cuit=column[6]
                )
    else:  # model == 'productos'
        queryset = Producto.objects.all()
        if len(queryset) > 0:
            print("ya hay " + str(len(queryset)) +
                  " clientes en la base de datos")
        else:
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                last_position = len(column) - 1
                detalle = column[1]
                if(last_position > 12):
                    iterations = last_position - 12
                    for i in range(iterations):
                        detalle = detalle + ", " + column[i + 2]
                    detalle = detalle[1:len(detalle)-1]

                Producto.objects.create(
                    codigo=column[0],
                    detalle=detalle,
                    stock=column[last_position - 10],
                    precio_costo=column[last_position - 9],
                    desc1=column[last_position - 8],
                    desc2=column[last_position - 7],
                    desc3=column[last_position - 6],
                    desc4=column[last_position - 5],
                    flete=column[last_position - 4],
                    ganancia=column[last_position - 3],
                    iva=column[last_position - 2],
                    agregado_cta_cte=column[last_position - 1],
                    categoria=column[last_position]
                )

    return redirect('/lubricentro_myc/acciones_csv')


def exportar_csv(request):
    model = request.GET['model']
    if model == 'clientes':
        queryset = Cliente.objects.all()
    else:  # model == 'productos'
        queryset = Producto.objects.all()

    f = io.StringIO()
    writer = csv.writer(f)
    row = []
    for key in queryset.values()[0].keys():
        row.append(key)
    writer.writerow(row)

    for s in queryset.values():
        row = []
        for value in s.values():
            row.append(value)
        writer.writerow(row)

    f.seek(0)
    response = HttpResponse(f, content_type='text/csv')
    content_disposition = 'attachment; filename=' + queryset.model.__name__ + 's.csv'
    response['Content-Disposition'] = content_disposition
    return response
