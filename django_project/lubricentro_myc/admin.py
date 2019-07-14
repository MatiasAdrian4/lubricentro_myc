from django.contrib import admin

from .models import Cliente, Producto

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Cliente._meta.get_fields()]
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Producto._meta.get_fields()]
