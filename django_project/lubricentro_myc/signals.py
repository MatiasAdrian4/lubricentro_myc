import datetime

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from lubricentro_myc.models import ProductCostHistory
from lubricentro_myc.models.invoice import ElementoRemito
from lubricentro_myc.models.product import Producto


@receiver(pre_save, sender=ElementoRemito)
def save_invoice_item(sender, instance, **kwargs):
    new_quantity = None
    if instance.id:  # an existent invoice item is being updated
        older_instance = ElementoRemito.objects.get(id=instance.id)
        if instance.cantidad != older_instance.cantidad:
            new_quantity = instance.cantidad - older_instance.cantidad
    else:  # a new invoice item is being created
        new_quantity = instance.cantidad
    if new_quantity:
        product = Producto.objects.get(codigo=instance.producto.codigo)
        product.stock -= new_quantity
        product.save()


@receiver(post_delete, sender=ElementoRemito)
def delete_invoice_item(sender, instance, **kwargs):
    product = Producto.objects.get(codigo=instance.producto.codigo)
    product.stock += instance.cantidad
    product.save()


@receiver(pre_save, sender=Producto)
def save_product(sender, instance, **kwargs):
    if not instance.codigo:
        return

    product_being_updated = Producto.objects.get(codigo=instance.codigo)
    old_price = product_being_updated.precio_costo
    new_price = instance.precio_costo

    if old_price != new_price:
        ProductCostHistory.objects.create(
            product=product_being_updated,
            old_price=old_price,
            new_price=new_price,
            timestamp=datetime.datetime.utcnow(),
        )
