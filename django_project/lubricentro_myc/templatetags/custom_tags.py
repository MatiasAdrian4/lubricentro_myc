from django import template
from lubricentro_myc.models.invoice import ElementoRemito

register = template.Library()


@register.simple_tag
def check_pagado(request, remito_id):
    elem_remitos = ElementoRemito.objects.filter(remito=remito_id, pagado=False)
    if len(elem_remitos) == 0:
        return True
    else:
        return False
