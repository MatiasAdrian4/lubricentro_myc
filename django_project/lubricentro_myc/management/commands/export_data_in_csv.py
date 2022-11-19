import csv
import logging

from django.core.management import BaseCommand
from lubricentro_myc.models import (
    Cliente,
    ElementoRemito,
    Producto,
    ProductPriceHistory,
    Remito,
    Venta,
)

logger = logging.getLogger("django")

DELIMITER = "|"


def export_file(filename: str, queryset):
    f = open(f"files/{filename}", "w")
    writer = csv.writer(f, delimiter=DELIMITER)
    for obj in queryset:
        writer.writerow(obj.data)


class Command(BaseCommand):
    help = "Exportes models data in a CSV file"

    def handle(self, *args, **kwargs):
        logger.info("Starting to export models data...")

        logger.info("Saving products...")
        export_file("products", Producto.objects.all())
        logger.info("Saving product prices history...")
        export_file("product_prices_history", ProductPriceHistory.objects.all())
        logger.info("Saving clients...")
        export_file("clients", Cliente.objects.all())
        logger.info("Saving sales...")
        export_file("sales", Venta.objects.all())
        logger.info("Saving invoices...")
        export_file("invoices", Remito.objects.all())
        logger.info("Saving invoice items...")
        export_file("invoice_items", ElementoRemito.objects.all())

        logger.info("Finished.")
