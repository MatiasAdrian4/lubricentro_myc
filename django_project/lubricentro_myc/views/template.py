# TODO:
#   This views will be removed. I need to move the required logic to their corresponding views.
#
import csv
import io

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView
from lubricentro_myc.models.client import Cliente
from lubricentro_myc.models.invoice import ElementoRemito, Remito
from lubricentro_myc.models.product import Producto
from lubricentro_myc.models.sale import Venta


def ventas(request):
    host = request.scheme + "://" + request.META["HTTP_HOST"]
    context = {"host": host}
    return render(request, "ventas.html", context=context)


def remitos_facturacion(request):
    context = {}
    return render(request, "remitos_facturacion.html", context=context)


class ImpresionStock(TemplateView):
    template_name = "impresion_stock.html"

    def get_context_data(self, **kwargs):
        context = super(ImpresionStock, self).get_context_data(**kwargs)
        categorias = Producto.objects.order_by().values("categoria").distinct()
        context["categorias"] = categorias
        return context


class CSV(TemplateView):
    template_name = "csv.html"


class Inventario(ListView):
    model = Producto
    template_name = "inventario.html"

    def get_queryset(self):
        args = self.request.GET
        queryset = []
        if "codigo" in args.keys():
            if args["codigo"] == "undefined":
                return []
            else:
                try:
                    producto = Producto.objects.get(codigo=args["codigo"])
                except Producto.DoesNotExist:
                    return []
            queryset.append(producto)
            return queryset
        elif "detalle" in args.keys():
            if len(args["detalle"].strip()) == 0:
                return []
            return Producto.objects.filter(detalle__icontains=args["detalle"]).order_by(
                "codigo"
            )
        elif "categoria" in args.keys():
            return Producto.objects.filter(categoria=args["categoria"]).order_by(
                "codigo"
            )
        else:
            return queryset

    def get_context_data(self, **kwargs):
        context = super(Inventario, self).get_context_data(**kwargs)
        context["url"] = self.request.build_absolute_uri(self.request.path)
        categorias = Producto.objects.order_by().values("categoria").distinct()
        context["categorias"] = categorias
        return context


class ListadoClientes(ListView):
    model = Cliente
    template_name = "listado_clientes.html"

    def get_queryset(self):
        args = self.request.GET
        queryset = []
        if "codigo" in args.keys():
            try:
                cliente = Cliente.objects.get(id=args["codigo"])
            except Cliente.DoesNotExist:
                return []
            queryset.append(cliente)
            return queryset
        elif "nombre" in args.keys():
            if len(args["nombre"].strip()) == 0:
                return []
            return Cliente.objects.filter(nombre__icontains=args["nombre"]).order_by(
                "id"
            )
        else:
            return Cliente.objects.all().order_by("id")

    def get_context_data(self, **kwargs):
        context = super(ListadoClientes, self).get_context_data(**kwargs)
        context["url"] = self.request.build_absolute_uri(self.request.path)
        return context


class Remitos(ListView):
    model = Remito
    template_name = "remitos.html"

    def get_queryset(self):
        args = self.request.GET
        queryset = []
        if "codigo" in args.keys():
            try:
                remito = Remito.objects.get(codigo=args["codigo"])
            except Remito.DoesNotExist:
                return []
            queryset.append(remito)
            return queryset
        elif "cliente" in args.keys():
            if len(args["cliente"].strip()) == 0:
                return []
            return Remito.objects.filter(
                cliente__nombre__icontains=args["cliente"]
            ).order_by("-codigo")
        else:
            return Remito.objects.all().order_by("-codigo")

    def get_context_data(self, **kwargs):
        context = super(Remitos, self).get_context_data(**kwargs)
        context["host"] = self.request.scheme + "://" + self.request.META["HTTP_HOST"]
        context["url"] = self.request.build_absolute_uri(self.request.path)
        return context


class RemitosEdicion(ListView):
    model = Producto
    template_name = "remitos_edicion.html"

    def get_queryset(self):
        args = self.request.GET
        queryset = []
        if "codigo" in args.keys():
            if args["codigo"] == "undefined":
                return []
            else:
                try:
                    remito = Remito.objects.get(codigo=args["codigo"])
                except Producto.DoesNotExist:
                    return []
            for elemento_remito in ElementoRemito.objects.filter(
                remito_id=remito.codigo
            ):
                elem_remito = {}
                if not elemento_remito.pagado:
                    elem_remito["id"] = elemento_remito.id
                    elem_remito["producto_id"] = elemento_remito.producto.codigo
                    elem_remito["producto_detalle"] = elemento_remito.producto.detalle
                    elem_remito["cantidad"] = elemento_remito.cantidad
                    queryset.append(elem_remito)
            return queryset
        else:
            return queryset

    def get_context_data(self, **kwargs):
        context = super(RemitosEdicion, self).get_context_data(**kwargs)
        args = self.request.GET
        if "codigo" in args.keys():
            context["nro_remito"] = args["codigo"]
        context["url"] = self.request.build_absolute_uri(self.request.path)
        return context


class HistorialVentas(ListView):
    model = Venta
    template_name = "ventas_historial.html"

    def get_queryset(self):
        args = self.request.GET
        if "fecha" in args.keys():
            return Venta.objects.filter(
                fecha__day=int(args["fecha"][0:2]),
                fecha__month=int(args["fecha"][3:5]),
                fecha__year=int(args["fecha"][6:10]),
            ).order_by("fecha")
        elif "mes" in args.keys():
            return Venta.objects.filter(
                fecha__month=int(args["mes"][0:2]), fecha__year=int(args["mes"][3:7])
            ).order_by("fecha")
        else:
            return []

    def get_context_data(self, **kwargs):
        context = super(HistorialVentas, self).get_context_data(**kwargs)
        ventas = self.get_queryset()
        total = 0
        for venta in ventas:
            total += venta.precio
        context["total"] = total
        return context


def importar_csv(request):
    model = request.POST.get("model", "")
    if model == "":
        return redirect("/lubricentro_myc/acciones_csv")

    if model == "clientes":
        queryset = Cliente.objects.all()
        if len(queryset) > 0:
            print("ya hay " + str(len(queryset)) + " clientes en la base de datos")
        else:
            csv_file = request.FILES["file"]
            if not csv_file.name.endswith(".csv"):
                messages.error(request, "THIS IS NOT A CSV FILE")
            data_set = csv_file.read().decode("UTF-8")
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=",", quotechar="|"):
                Cliente.objects.create(
                    id=column[0],
                    nombre=column[1],
                    direccion=column[2],
                    localidad=column[3],
                    codigo_postal=column[4],
                    telefono=column[5],
                    cuit=column[6],
                )
    else:  # model == 'productos'
        queryset = Producto.objects.all()
        if len(queryset) > 0:
            print("ya hay " + str(len(queryset)) + " clientes en la base de datos")
        else:
            csv_file = request.FILES["file"]
            if not csv_file.name.endswith(".csv"):
                messages.error(request, "THIS IS NOT A CSV FILE")
            data_set = csv_file.read().decode("UTF-8")
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=",", quotechar="|"):
                last_position = len(column) - 1
                detalle = column[1]
                if last_position > 12:
                    iterations = last_position - 12
                    for i in range(iterations):
                        detalle = detalle + ", " + column[i + 2]
                    detalle = detalle[1 : len(detalle) - 1]

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
                    categoria=column[last_position],
                )

    return redirect("/lubricentro_myc/acciones_csv")


def exportar_csv(request):
    model = request.GET["model"]
    if model == "clientes":
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
    response = HttpResponse(f, content_type="text/csv")
    content_disposition = "attachment; filename=" + queryset.model.__name__ + "s.csv"
    response["Content-Disposition"] = content_disposition
    return response
