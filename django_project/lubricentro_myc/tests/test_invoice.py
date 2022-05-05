import json
from unittest.mock import MagicMock, patch

from django.test import TestCase
from lubricentro_myc.models.invoice import ElementoRemito, Remito
from lubricentro_myc.models.product import Producto
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
        cls.client_url = "/lubricentro_myc/remito"
        cls.client = ClientFactory()
        cls.product_1 = ProductFactory(stock=5.0)
        cls.product_2 = ProductFactory(stock=11.5)
        cls.invoice = InvoiceFactory(cliente=cls.client)
        InvoiceItemFactory(remito=cls.invoice, producto=cls.product_1, cantidad=1.5)
        InvoiceItemFactory(remito=cls.invoice, producto=cls.product_2, cantidad=7.0)

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_delete_invoice(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)
        self.client.get(
            f"{self.client_url}/borrar_remito?codigo={self.invoice.codigo}", follow=True
        )
        invoice = Remito.objects.filter(codigo=self.invoice.codigo).first()
        invoice_items = ElementoRemito.objects.filter(remito=self.invoice)
        products = Producto.objects.all()
        self.assertIsNone(invoice)
        self.assertEqual(len(invoice_items), 0)
        self.assertEqual(products[0].stock, 6.5)
        self.assertEqual(products[1].stock, 18.5)


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
            remito=cls.invoice_1, producto_id=cls.product_1.codigo, cantidad=1
        )
        cls.invoice_item_2 = InvoiceItemFactory(
            remito=cls.invoice_1, producto_id=cls.product_1.codigo, cantidad=1
        )
        cls.invoice_item_3 = InvoiceItemFactory(
            remito=cls.invoice_1, producto_id=cls.product_1.codigo, cantidad=1
        )
        cls.invoice_item_4 = InvoiceItemFactory(
            remito=cls.invoice_2, producto_id=cls.product_1.codigo, cantidad=1
        )
        cls.invoice_item_5 = InvoiceItemFactory(
            remito=cls.invoice_2, producto_id=cls.product_2.codigo, cantidad=1
        )

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_search_by_client_code(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)
        response = self.client.get(
            f"{self.client_url}/buscar_por_codigo_cliente?codigo={self.client_1.id}",
            follow=True,
        )
        invoice_items = json.loads(response.content)["elementos_remito"]
        self.assertEqual(len(invoice_items), 3)
        self.assertEqual(invoice_items[0]["elem_remito"], self.invoice_item_1.id)
        self.assertEqual(invoice_items[1]["elem_remito"], self.invoice_item_2.id)
        self.assertEqual(invoice_items[2]["elem_remito"], self.invoice_item_3.id)

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_marked_items_as_paid(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)
        self.client.post(
            f"{self.client_url}/marcar_pagados/",
            json.dumps({"elementos": [self.invoice_item_1.id, self.invoice_item_2.id]}),
            content_type="application/json",
            follow=True,
        )
        items = ElementoRemito.objects.all().order_by("id")
        self.assertTrue(items[0].pagado)
        self.assertTrue(items[1].pagado)
        self.assertFalse(items[2].pagado)

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_store_items(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)
        self.client.post(
            f"{self.client_url}/guardar_elementos/",
            json.dumps(
                {
                    "elementos": [
                        {
                            "producto": self.product_1.codigo,
                            "remito": self.invoice_3.codigo,
                            "cantidad": 3.5,
                        },
                        {
                            "producto": self.product_2.codigo,
                            "remito": self.invoice_3.codigo,
                            "cantidad": 2.0,
                        },
                    ]
                }
            ),
            content_type="application/json",
            follow=True,
        )
        invoice_items = ElementoRemito.objects.filter(remito=self.invoice_3)
        self.assertEqual(len(invoice_items), 2)
        self.assertEqual(invoice_items[0].producto.codigo, self.product_1.codigo)
        self.assertEqual(invoice_items[0].remito.codigo, self.invoice_3.codigo)
        self.assertEqual(invoice_items[0].cantidad, 3.5)
        self.assertEqual(invoice_items[1].producto.codigo, self.product_2.codigo)
        self.assertEqual(invoice_items[1].remito.codigo, self.invoice_3.codigo)
        self.assertEqual(invoice_items[1].cantidad, 2.0)

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_update_items(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)
        self.client.post(
            f"{self.client_url}/modificar_cantidad/",
            json.dumps(
                {
                    "elementos": [
                        {
                            "id": self.invoice_item_1.id,
                            "cantidad": 4.5,
                        },
                        {
                            "id": self.invoice_item_5.id,
                            "cantidad": 0.5,
                        },
                    ]
                }
            ),
            content_type="application/json",
            follow=True,
        )
        product_1 = Producto.objects.get(codigo=self.product_1.codigo)
        product_2 = Producto.objects.get(codigo=self.product_2.codigo)
        self.assertEqual(product_1.stock, 1.5)
        self.assertEqual(product_2.stock, 8.0)
