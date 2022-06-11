from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from lubricentro_myc.models.invoice import ElementoRemito
from lubricentro_myc.models.product import Producto


@receiver(pre_save, sender=ElementoRemito)
def save_invoice_item(sender, instance, **kwargs):
    new_quantity = None
    older = instance
    if older.id:  # an existent invoice item is being updated
        newer = ElementoRemito.objects.get(id=instance.id)
        if older.cantidad != newer.cantidad:
            new_quantity = older.cantidad - newer.cantidad
    else:  # a new invoice item is being created
        new_quantity = older.cantidad
    if new_quantity:
        producto = Producto.objects.get(codigo=older.producto.codigo)
        producto.stock -= new_quantity
        producto.save()


@receiver(post_delete, sender=ElementoRemito)
def delete_invoice_item(sender, instance, **kwargs):
    producto = Producto.objects.get(codigo=instance.producto.codigo)
    producto.stock += instance.cantidad
    producto.save()
