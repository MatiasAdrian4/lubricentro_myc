import json
from unittest.mock import MagicMock, patch

from django.test import TestCase
from lubricentro_myc.tests.factories import (
    ClientFactory,
    InvoiceFactory,
    InvoiceItemFactory,
    ProductFactory,
)
from rest_framework.test import APIClient


class InvoiceItemTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()
        cls.client_url = "/lubricentro_myc/elementos_remito"
        cls.client_1 = ClientFactory(nombre="Juan")
        cls.client_2 = ClientFactory(nombre="Pedro")
        cls.product_1 = ProductFactory(stock=5.0)
        cls.product_2 = ProductFactory(stock=7.5)
        cls.invoice_1 = InvoiceFactory(cliente=cls.client_1)
        cls.invoice_2 = InvoiceFactory(cliente=cls.client_2)
        cls.invoice_3 = InvoiceFactory(cliente=cls.client_2)
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

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_search_by_client_code(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)
        response = self.client.get(
            f"{self.client_url}?codigo_cliente={self.client_1.id}",
            follow=True,
        )
        invoice_items = response.data
        self.assertEqual(len(invoice_items), 3)
        self.assertEqual(invoice_items[0]["id"], self.invoice_item_1.id)
        self.assertEqual(invoice_items[1]["id"], self.invoice_item_2.id)
        self.assertEqual(invoice_items[2]["id"], self.invoice_item_3.id)

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_search_by_paid(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)
        response = self.client.get(
            f"{self.client_url}?pago=true",
            follow=True,
        )
        invoice_items = response.data
        self.assertEqual(len(invoice_items), 2)
        self.assertEqual(invoice_items[0]["id"], self.invoice_item_1.id)
        self.assertEqual(invoice_items[1]["id"], self.invoice_item_3.id)

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_update_dont_allow_to_update_invoice(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)
        response = self.client.patch(
            f"{self.client_url}/{self.invoice_item_1.id}/",
            json.dumps({"producto": self.product_2.codigo}),
            content_type="application/json",
            follow=True,
        )
        self.assertEqual(response.status_code, 400)

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_update_dont_allow_to_update_product(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)
        response = self.client.patch(
            f"{self.client_url}/{self.invoice_item_1.id}/",
            json.dumps({"remito": self.invoice_2.codigo}),
            content_type="application/json",
            follow=True,
        )
        self.assertEqual(response.status_code, 400)
