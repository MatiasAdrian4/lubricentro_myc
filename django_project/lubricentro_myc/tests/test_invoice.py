import json
from unittest.mock import MagicMock, patch

from django.test import TestCase
from lubricentro_myc.models.invoice import ElementoRemito, Remito
from lubricentro_myc.tests.factories import (
    ClientFactory,
    InvoiceFactory,
    InvoiceItemFactory,
    ProductFactory,
)
from rest_framework.test import APIClient


class InvoiceTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()
        cls.client_url = "/lubricentro_myc/remitos"
        cls.client_1 = ClientFactory(nombre="Juan")
        cls.client_2 = ClientFactory(nombre="Pedro")
        cls.client_3 = ClientFactory(nombre="Jose")
        cls.product_1 = ProductFactory(stock=5.0)
        cls.product_2 = ProductFactory(stock=11.5)
        cls.invoice_1 = InvoiceFactory(cliente=cls.client_1)
        cls.invoice_2 = InvoiceFactory(cliente=cls.client_3)
        InvoiceItemFactory(remito=cls.invoice_1, producto=cls.product_1, cantidad=1.5)
        InvoiceItemFactory(remito=cls.invoice_1, producto=cls.product_2, cantidad=7.0)

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_list_invoices_by_clients_name(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)
        response = self.client.get(f"{self.client_url}?nombre=jua", follow=True)
        invoices = response.data["results"]
        self.assertEqual(len(invoices), 1)
        self.assertEqual(invoices[0]["cliente"], "Juan")

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_store_invoice_items(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)
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
