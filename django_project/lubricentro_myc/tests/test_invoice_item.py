import json

from django.test import TestCase
from lubricentro_myc.models import ElementoRemito, Venta
from lubricentro_myc.tests.factories import (
    ClientFactory,
    InvoiceFactory,
    InvoiceItemFactory,
    ProductFactory,
)
from lubricentro_myc.utils import mock_auth
from rest_framework.test import APIClient


class InvoiceItemTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()
        cls.client_url = "/lubricentro_myc/elementos_remito"
        cls.client_1 = ClientFactory(nombre="Juan")
        cls.client_2 = ClientFactory(nombre="Pedro")
        cls.client_3 = ClientFactory(nombre="Matias")
        cls.product_1 = ProductFactory(codigo=1, stock=5.0)
        cls.product_2 = ProductFactory(codigo=2, stock=7.5)
        cls.product_3 = ProductFactory(codigo=3, stock=3.0)
        cls.invoice_1 = InvoiceFactory(cliente=cls.client_1)
        cls.invoice_2 = InvoiceFactory(cliente=cls.client_2)
        cls.invoice_3 = InvoiceFactory(cliente=cls.client_2)
        cls.invoice_4 = InvoiceFactory(cliente=cls.client_3)
        cls.invoice_item_1 = InvoiceItemFactory(
            remito=cls.invoice_1,
            producto_id=cls.product_1.codigo,
            cantidad=1,
            pagado=True,
        )
        cls.invoice_item_2 = InvoiceItemFactory(
            remito=cls.invoice_1,
            producto_id=cls.product_1.codigo,
            cantidad=1,
            pagado=False,
        )
        cls.invoice_item_3 = InvoiceItemFactory(
            remito=cls.invoice_1,
            producto_id=cls.product_1.codigo,
            cantidad=1,
            pagado=True,
        )
        cls.invoice_item_4 = InvoiceItemFactory(
            remito=cls.invoice_2,
            producto_id=cls.product_1.codigo,
            cantidad=1,
            pagado=False,
        )
        cls.invoice_item_5 = InvoiceItemFactory(
            remito=cls.invoice_2,
            producto_id=cls.product_2.codigo,
            cantidad=1,
            pagado=False,
        )
        cls.invoice_item_6 = InvoiceItemFactory(
            remito=cls.invoice_4,
            producto_id=cls.product_1.codigo,
            cantidad=5.0,
            pagado=False,
        )
        cls.invoice_item_7 = InvoiceItemFactory(
            remito=cls.invoice_4,
            producto_id=cls.product_2.codigo,
            cantidad=2.0,
            pagado=False,
        )
        cls.invoice_item_8 = InvoiceItemFactory(
            remito=cls.invoice_4,
            producto_id=cls.product_3.codigo,
            cantidad=8.0,
            pagado=False,
        )

    @mock_auth
    def test_search_by_client_code(self):
        response = self.client.get(
            f"{self.client_url}?codigo_cliente={self.client_1.id}",
            follow=True,
        )
        invoice_items = response.data
        self.assertEqual(len(invoice_items), 3)
        self.assertEqual(invoice_items[0]["id"], self.invoice_item_1.id)
        self.assertEqual(invoice_items[1]["id"], self.invoice_item_2.id)
        self.assertEqual(invoice_items[2]["id"], self.invoice_item_3.id)

    @mock_auth
    def test_search_by_paid(self):
        response = self.client.get(
            f"{self.client_url}?pago=true",
            follow=True,
        )
        invoice_items = response.data
        self.assertEqual(len(invoice_items), 2)
        self.assertEqual(invoice_items[0]["id"], self.invoice_item_1.id)
        self.assertEqual(invoice_items[1]["id"], self.invoice_item_3.id)

    @mock_auth
    def test_update_dont_allow_to_update_invoice(self):
        response = self.client.patch(
            f"{self.client_url}/{self.invoice_item_1.id}/",
            json.dumps({"producto": self.product_2.codigo}),
            content_type="application/json",
            follow=True,
        )
        self.assertEqual(response.status_code, 400)

    @mock_auth
    def test_update_dont_allow_to_update_product(self):
        response = self.client.patch(
            f"{self.client_url}/{self.invoice_item_1.id}/",
            json.dumps({"remito": self.invoice_2.codigo}),
            content_type="application/json",
            follow=True,
        )
        self.assertEqual(response.status_code, 400)

    @mock_auth
    def test_billing(self):
        invoice_item_ids = [
            self.invoice_item_6.id,
            self.invoice_item_7.id,
            self.invoice_item_8.id,
        ]
        response = self.client.post(
            f"{self.client_url}/bulk/",
            json.dumps(
                {
                    "items": invoice_item_ids,
                }
            ),
            content_type="application/json",
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            ElementoRemito.objects.filter(
                id__in=invoice_item_ids, pagado=False
            ).count(),
            0,
        )

        self.assertTrue(
            Venta.objects.filter(
                producto=self.invoice_item_6.producto,
                cantidad=self.invoice_item_6.cantidad,
            ).exists()
        )
        self.assertTrue(
            Venta.objects.filter(
                producto=self.invoice_item_7.producto,
                cantidad=self.invoice_item_7.cantidad,
            ).exists()
        )
        self.assertTrue(
            Venta.objects.filter(
                producto=self.invoice_item_7.producto,
                cantidad=self.invoice_item_7.cantidad,
            ).exists()
        )
