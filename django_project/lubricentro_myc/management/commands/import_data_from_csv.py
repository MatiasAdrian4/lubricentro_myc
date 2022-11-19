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


def get_reader(filename: str, store_data):
    with open(f"files/{filename}.csv", "r") as file:
        csv_reader = csv.reader(file, delimiter=DELIMITER)
        store_data(csv_reader)


def store_products():
    def store_data(reader):
        products = []
        for row in reader:
            products.append(
                Producto(
                    codigo=row[0],
                    codigo_en_pantalla=row[1],
                    detalle=row[2],
                    stock=row[3],
                    precio_costo=row[4],
                    desc1=row[5],
                    desc2=row[6],
                    desc3=row[7],
                    desc4=row[8],
                    flete=row[9],
                    ganancia=row[10],
                    iva=row[11],
                    agregado_cta_cte=row[12],
                    categoria=row[13],
                )
            )
        Producto.objects.all().delete()
        Producto.objects.bulk_create(products)

    get_reader("products", store_data)


def store_product_prices_history():
    def store_data(reader):
        product_prices_history = []
        for row in reader:
            product_prices_history.append(
                ProductPriceHistory(
                    id=row[0],
                    product=Producto.objects.get(codigo=row[1]),
                    old_price=row[2],
                    new_price=row[3],
                    timestamp=row[4],
                )
            )
        ProductPriceHistory.objects.all().delete()
        ProductPriceHistory.objects.bulk_create(product_prices_history)

    get_reader("product_prices_history", store_data)


def store_clients():
    def store_data(reader):
        clients = []
        for row in reader:
            clients.append(
                Cliente(
                    id=row[0],
                    nombre=row[1],
                    direccion=row[2],
                    localidad=row[3],
                    codigo_postal=row[4],
                    telefono=row[5],
                    cuit=row[6],
                    email=row[7],
                )
            )
        Cliente.objects.all().delete()
        Cliente.objects.bulk_create(clients)

    get_reader("clients", store_data)


def store_sales():
    def store_data(reader):
        sales = []
        for row in reader:
            sales.append(
                Venta(
                    id=row[0],
                    producto=Producto.objects.get(codigo=row[1]),
                    cantidad=row[2],
                    precio=row[3],
                    fecha=row[4],
                )
            )
        Venta.objects.all().delete()
        Venta.objects.bulk_create(sales)

    get_reader("sales", store_data)


def store_invoices():
    def store_data(reader):
        invoices = []
        for row in reader:
            invoices.append(
                Remito(
                    codigo=row[0], cliente=Cliente.objects.get(id=row[1]), fecha=row[2]
                )
            )
        Remito.objects.all().delete()
        Remito.objects.bulk_create(invoices)

    get_reader("invoices", store_data)


def store_invoice_items():
    def store_data(reader):
        invoice_items = []
        for row in reader:
            invoice_items.append(
                ElementoRemito(
                    id=row[0],
                    remito=Remito.objects.get(codigo=row[1]),
                    producto=Producto.objects.get(codigo=row[2]),
                    cantidad=row[3],
                    pagado=row[4],
                )
            )
        ElementoRemito.objects.all().delete()
        ElementoRemito.objects.bulk_create(invoice_items)

    get_reader("invoice_items", store_data)


class Command(BaseCommand):
    help = "Imports models data from a CSV file"

    def handle(self, *args, **kwargs):
        logger.info("Starting to import models data...")

        logger.info("Storing products...")
        store_products()
        logger.info("Storing product prices history...")
        store_product_prices_history()
        logger.info("Storing clients...")
        store_clients()
        logger.info("Storing sales...")
        store_sales()
        logger.info("Storing invoices...")
        store_invoices()
        logger.info("Storing invoice items...")
        store_invoice_items()

        logger.info("Finished.")
