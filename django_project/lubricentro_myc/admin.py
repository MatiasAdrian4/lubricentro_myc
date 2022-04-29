from django.contrib import admin

from .models import Cliente, ElementoRemito, Producto, Remito, Venta


def download_csv(modeladmin, request, queryset):
    import csv
    from io import StringIO

    from django.http import HttpResponse

    f = StringIO()
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


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "nombre",
        "direccion",
        "localidad",
        "codigo_postal",
        "telefono",
        "cuit",
    ]
    actions = [download_csv]
    download_csv.short_description = "Download CSV file for selected items"


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = [
        "codigo",
        "detalle",
        "stock",
        "precio_costo",
        "desc1",
        "desc2",
        "desc3",
        "desc4",
        "flete",
        "ganancia",
        "iva",
        "agregado_cta_cte",
        "categoria",
        "precio_venta_contado",
        "precio_venta_cta_cte",
    ]
    actions = [download_csv]
    download_csv.short_description = "Download CSV file for selected items"


@admin.register(Remito)
class RemitoAdmin(admin.ModelAdmin):
    list_display = ["codigo", "fecha"]


@admin.register(ElementoRemito)
class ElementoRemitoAdmin(admin.ModelAdmin):
    list_display = ["id", "remito", "producto", "cantidad", "pagado"]


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ["producto", "cantidad", "precio", "fecha"]
