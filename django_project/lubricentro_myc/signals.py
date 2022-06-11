from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from lubricentro_myc.models.invoice import ElementoRemito
from lubricentro_myc.models.product import Producto


@receiver(pre_save, sender=ElementoRemito)
def save_invoice_item(sender, instance, **kwargs):
    older = instance
    newer = ElementoRemito.objects.get(id=instance.id)
    # continue
    pass


@receiver(post_delete, sender=ElementoRemito)
def delete_invoice_item(sender, instance, **kwargs):
    producto = Producto.objects.get(codigo=instance.producto.codigo)
    producto.stock += instance.cantidad
    producto.save()
