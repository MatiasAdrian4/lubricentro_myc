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


def create_file(filename: str, queryset):
    f = open(f"files/{filename}.csv", "w")
    writer = csv.writer(f, delimiter=DELIMITER)
    for obj in queryset:
        writer.writerow(obj.data)


class Command(BaseCommand):
    help = "Exports models data in a CSV file"

    def handle(self, *args, **kwargs):
        logger.info("Starting to export models data...")

        logger.info("Saving products...")
        create_file("products", Producto.objects.all())
        logger.info("Saving product prices history...")
        create_file("product_prices_history", ProductPriceHistory.objects.all())
        logger.info("Saving clients...")
        create_file("clients", Cliente.objects.all())
        logger.info("Saving sales...")
        create_file("sales", Venta.objects.all())
        logger.info("Saving invoices...")
        create_file("invoices", Remito.objects.all())
        logger.info("Saving invoice items...")
        create_file("invoice_items", ElementoRemito.objects.all())

        logger.info("Finished.")
