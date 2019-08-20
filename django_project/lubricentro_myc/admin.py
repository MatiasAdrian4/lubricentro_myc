from django.contrib import admin

from .models import Cliente, Producto, ElementoRemito

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id','nombre','direccion','localidad','codigo_postal','telefono','cuit']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo','detalle','stock','precio_costo','precio_venta_contado','precio_venta_cta_cte', 'categoria', 'desc1', 'desc2', 'desc3', 'desc4']

@admin.register(ElementoRemito)
class ElementoRemitoAdmin(admin.ModelAdmin):
    list_display = ['numero_remito','producto','cantidad']