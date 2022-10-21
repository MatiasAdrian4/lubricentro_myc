import json

from django.test import TestCase
from lubricentro_myc.models.invoice import ElementoRemito, Remito
from lubricentro_myc.models.product import Producto
from lubricentro_myc.tests.factories import (
    ClientFactory,
    InvoiceFactory,
    InvoiceItemFactory,
    ProductFactory,
)
from lubricentro_myc.utils import mock_auth
from rest_framework.test import APIClient


class InvoiceTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()
        cls.client_url = "/lubricentro_myc/remitos"

        cls.client_1 = ClientFactory(nombre="Juan")
        cls.client_2 = ClientFactory(nombre="Pedro")
        cls.client_3 = ClientFactory(nombre="Jose")
        cls.client_4 = ClientFactory(nombre="Enrique")

        cls.product_1 = ProductFactory(codigo=1, stock=5.0)
        cls.product_2 = ProductFactory(codigo=2, stock=11.5)
        cls.product_3 = ProductFactory(codigo=3, stock=130.65)
        cls.product_4 = ProductFactory(codigo=4, stock=62)
        cls.product_5 = ProductFactory(codigo=5, stock=201.5)

        cls.invoice_1 = InvoiceFactory(cliente=cls.client_1)
        cls.invoice_2 = InvoiceFactory(cliente=cls.client_3)
        cls.invoice_3 = InvoiceFactory(cliente=cls.client_4)

        InvoiceItemFactory(remito=cls.invoice_1, producto=cls.product_1, cantidad=1.5)
        InvoiceItemFactory(remito=cls.invoice_1, producto=cls.product_2, cantidad=7.0)
        cls.invoice_item_3 = InvoiceItemFactory(
            remito=cls.invoice_3,
            producto=cls.product_3,
            cantidad=1,
            pagado=False,
        )
        cls.invoice_item_4 = InvoiceItemFactory(
            remito=cls.invoice_3,
            producto=cls.product_4,
            cantidad=1,
            pagado=False,
        )
        cls.invoice_item_5 = InvoiceItemFactory(
            remito=cls.invoice_3,
            producto=cls.product_5,
            cantidad=1.5,
            pagado=False,
        )

    @mock_auth
    def test_list_invoices_by_clients_name(self):
        response = self.client.get(f"{self.client_url}?nombre=jua", follow=True)
        invoices = response.data["results"]
        self.assertEqual(len(invoices), 1)
        self.assertEqual(invoices[0]["cliente"], "Juan")

    @mock_auth
    def test_store_invoice_items(self):
        self.client.post(
            f"{self.client_url}/",
            json.dumps(
                {
                    "cliente": self.client_2.id,
                    "elementos_remito": [
                        {
                            "producto": self.product_1.codigo,
                            "cantidad": 3.5,
                        },
                        {
                            "producto": self.product_2.codigo,
                            "cantidad": 2.0,
                        },
                    ],
                }
            ),
            content_type="application/json",
            follow=True,
        )
        invoice = Remito.objects.filter(cliente=self.client_2).first()
        invoice_items = ElementoRemito.objects.filter(remito_id=invoice.codigo)
        self.assertEqual(len(invoice_items), 2)
        self.assertEqual(invoice_items[0].producto.codigo, self.product_1.codigo)
        self.assertEqual(invoice_items[0].remito.codigo, invoice.codigo)
        self.assertEqual(invoice_items[0].cantidad, 3.5)
        self.assertEqual(invoice_items[1].producto.codigo, self.product_2.codigo)
        self.assertEqual(invoice_items[1].remito.codigo, invoice.codigo)
        self.assertEqual(invoice_items[1].cantidad, 2.0)

    @mock_auth
    def test_update_invoice(self):
        self.client.patch(
            f"{self.client_url}/{self.invoice_3.codigo}/",
            json.dumps(
                {
                    "elementos_remito": [
                        {
                            "id": self.invoice_item_4.id,
                            "cantidad": 2,
                        },
                        {
                            "id": self.invoice_item_5.id,
                            "cantidad": 8,
                        },
                    ],
                }
            ),
            content_type="application/json",
            follow=True,
        )

        invoice = Remito.objects.get(codigo=self.invoice_3.codigo)
        invoice_items = {
            invoice_item["id"]: invoice_item["cantidad"]
            for invoice_item in invoice.resumen_elementos
        }

        self.assertNotIn(self.invoice_item_3.id, invoice_items)
        self.assertIn(self.invoice_item_4.id, invoice_items)
        self.assertIn(self.invoice_item_5.id, invoice_items)

        self.assertEqual(invoice_items[self.invoice_item_4.id], 2)
        self.assertEqual(invoice_items[self.invoice_item_5.id], 8)

        self.assertEqual(
            Producto.objects.get(codigo=self.product_3.codigo).stock, 130.65
        )
        self.assertEqual(Producto.objects.get(codigo=self.product_4.codigo).stock, 60)
        self.assertEqual(
            Producto.objects.get(codigo=self.product_5.codigo).stock, 193.5
        )
