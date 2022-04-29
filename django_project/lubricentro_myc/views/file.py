import csv
import io

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import get_template
from lubricentro_myc.models import Cliente, ElementoRemito, Producto, Remito
from lubricentro_myc.utils import render_to_pdf


def generar_stock_pdf(request, *args, **kwargs):
    template = get_template("pdf/stock_pdf.html")

    categoria = request.GET["categoria"]
    if categoria is not None:
        productos = Producto.objects.filter(categoria__iexact=categoria)
    else:
        productos = Producto.objects.none()
    total_precio_costo = 0.0
    total_precio_venta = 0.0
    for producto in productos:
        total_precio_costo += producto.precio_costo_con_descuentos * producto.stock
        total_precio_venta += producto.precio_venta_contado * producto.stock
    context = {
        "categoria": categoria,
        "productos": productos,
        "total_precio_costo": total_precio_costo,
        "total_precio_venta": total_precio_venta,
    }
    html = template.render(context)
    pdf = render_to_pdf("pdf/stock_pdf.html", context)
    if pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        filename = "stock_%s.pdf" % (categoria)
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename=%s" % (filename)
        response["Content-Disposition"] = content
        return response
    return HttpResponse("Not found")


def generar_remito_pdf(request, *args, **kwargs):
    template = get_template("pdf/remito_pdf.html")

    remito = Remito.objects.get(codigo=request.GET["cod_remito"])
    elementos_remito = []
    for elemento in ElementoRemito.objects.filter(remito=remito):
        producto = Producto.objects.get(codigo=elemento.producto_id)
        elemento_remito = {}
        elemento_remito["codigo"] = producto.codigo
        elemento_remito["detalle"] = producto.detalle
        elemento_remito["cantidad"] = elemento.cantidad
        elementos_remito.append(elemento_remito)
    context = {
        "remito": remito,
        "cliente": Cliente.objects.get(id=remito.cliente_id),
        "elementos_remito": elementos_remito,
    }
    html = template.render(context)
    pdf = render_to_pdf("pdf/remito_pdf.html", context)
    if pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        filename = "remito_%s.pdf" % ("editar_aca")
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename=%s" % (filename)
        response["Content-Disposition"] = content
        return response
    return HttpResponse("Not found")


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
