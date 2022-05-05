import json
from unittest.mock import MagicMock, patch

from django.test import TestCase
from lubricentro_myc.models.product import Producto
from lubricentro_myc.models.sale import Venta
from lubricentro_myc.tests.factories import ProductFactory, SaleFactory
from rest_framework.test import APIClient


class SaleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()
        cls.client_url = "/lubricentro_myc/ventas_realizadas"
        cls.product_1 = ProductFactory(codigo=1, stock=5)
        cls.product_2 = ProductFactory(codigo=2, stock=4)
        cls.mocked_sale = {
            "ventas": [
                {
                    "producto": cls.product_1.codigo,
                    "cantidad": 3,
                    "precio": "700",
                },
                {
                    "producto": cls.product_2.codigo,
                    "cantidad": 1,
                    "precio": "1500",
                },
            ]
        }

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_new_sale_without_updating_stock(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)
        self.client.post(
            f"{self.client_url}/guardar_venta/",
            json.dumps(self.mocked_sale),
            content_type="application/json",
            follow=True,
        )
        sales = Venta.objects.all()
        producto_1 = Producto.objects.get(codigo=self.product_1.codigo)
        producto_2 = Producto.objects.get(codigo=self.product_2.codigo)
        self.assertEqual(len(sales), 2)
        self.assertEqual(sales[0].producto.codigo, self.product_1.codigo)
        self.assertEqual(sales[1].producto.codigo, self.product_2.codigo)
        self.assertEqual(producto_1.stock, 5)
        self.assertEqual(producto_2.stock, 4)

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_new_sale_updating_stock(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)
        self.client.post(
            f"{self.client_url}/guardar_venta_y_actualizar_stock/",
            json.dumps(self.mocked_sale),
            content_type="application/json",
            follow=True,
        )
        sales = Venta.objects.all()
        producto_1 = Producto.objects.get(codigo=self.product_1.codigo)
        producto_2 = Producto.objects.get(codigo=self.product_2.codigo)
        self.assertEqual(len(sales), 2)
        self.assertEqual(sales[0].producto.codigo, self.product_1.codigo)
        self.assertEqual(sales[1].producto.codigo, self.product_2.codigo)
        self.assertEqual(producto_1.stock, 2)
        self.assertEqual(producto_2.stock, 3)

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_sales_per_year(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)

        SaleFactory(fecha="2021-03-12", precio=3500)
        SaleFactory(fecha="2021-05-05", precio=1750)
        SaleFactory(fecha="2021-04-29", precio=275)
        SaleFactory(fecha="2021-05-22", precio=1125)
        SaleFactory(fecha="2021-10-03", precio=2250)

        response = self.client.get(
            f"{self.client_url}/ventas_por_anio?year=2021", follow=True
        )
        ventas = json.loads(response.content)["sales_per_year"]
        self.assertEqual(
            ventas, [0, 0, 3500.0, 275.0, 2875.0, 0, 0, 0, 0, 2250.0, 0, 0]
        )

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_sales_per_month(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)

        SaleFactory(fecha="2021-05-12", precio=1050)
        SaleFactory(fecha="2021-05-05", precio=700)
        SaleFactory(fecha="2021-05-30", precio=2250)
        SaleFactory(fecha="2021-05-22", precio=1300)
        SaleFactory(fecha="2021-05-05", precio=2300)

        response = self.client.get(
            f"{self.client_url}/ventas_por_mes?month=5&year=2021", follow=True
        )
        ventas = json.loads(response.content)["sales_per_month"]
        self.assertEqual(
            ventas,
            [
                0,
                0,
                0,
                0,
                3000.0,
                0,
                0,
                0,
                0,
                0,
                0,
                1050.0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                1300.0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                2250.0,
                0,
            ],
        )
