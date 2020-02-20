from django.contrib import admin

from .models import Cliente, Producto, Remito, ElementoRemito, Venta


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'direccion',
                    'localidad', 'codigo_postal', 'telefono', 'cuit']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'detalle', 'stock', 'precio_costo', 'desc1', 'desc2', 'desc3', 'desc4', 'flete',
                    'ganancia', 'iva', 'agregado_cta_cte', 'categoria', 'precio_venta_contado', 'precio_venta_cta_cte']


@admin.register(Remito)
class RemitoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'fecha']


@admin.register(ElementoRemito)
class ElementoRemitoAdmin(admin.ModelAdmin):
    list_display = ['id', 'remito', 'producto', 'cantidad', 'pagado']


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['producto', 'cantidad', 'precio', 'fecha']
