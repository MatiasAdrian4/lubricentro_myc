from django.http import HttpResponse
from lubricentro_myc.models.client import Cliente
from lubricentro_myc.models.invoice import ElementoRemito, Remito
from lubricentro_myc.models.product import Producto
from lubricentro_myc.utils import render_to_pdf


def generar_stock_pdf(request):
    categoria = request.GET.get("categoria")
    if not categoria:
        return HttpResponse(status=400)
    productos = Producto.objects.filter(categoria__iexact=categoria)
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
    pdf = render_to_pdf("pdf/stock_pdf.html", context)
    if not pdf:
        return HttpResponse(status=500)
    response = HttpResponse(pdf, content_type="application/pdf")
    filename = f"stock_{categoria}.pdf"
    content = f"inline; filename='{filename}'"
    download = request.GET.get("download")
    if download:
        content = f"attachment; filename={filename}"
    response["Content-Disposition"] = content
    return response


def generar_remito_pdf(request):
    codigo_remito = request.GET.get("cod_remito")
    if not codigo_remito:
        return HttpResponse(status=400)
    try:
        remito = Remito.objects.get(codigo=codigo_remito)
    except Remito.DoesNotExist:
        return HttpResponse(status=404)
    elementos_remito = []
    for elemento in ElementoRemito.objects.filter(remito=remito):
        producto = Producto.objects.get(codigo=elemento.producto_id)
        elemento_remito = {
            "codigo": producto.codigo_en_pantalla,
            "detalle": producto.detalle,
            "cantidad": elemento.cantidad,
        }
        elementos_remito.append(elemento_remito)
    context = {
        "remito": remito,
        "cliente": Cliente.objects.get(id=remito.cliente_id),
        "elementos_remito": elementos_remito,
    }
    pdf = render_to_pdf("pdf/remito_pdf.html", context)
    if not pdf:
        return HttpResponse(status=500)
    response = HttpResponse(pdf, content_type="application/pdf")
    filename = f"remito_{codigo_remito}.pdf"
    content = f"inline; filename='{filename}'"
    download = request.GET.get("download")
    if download:
        content = f"attachment; filename={filename}"
    response["Content-Disposition"] = content
    return response
