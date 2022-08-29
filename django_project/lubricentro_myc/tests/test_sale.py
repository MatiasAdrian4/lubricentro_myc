import json

from django.test import TestCase
from lubricentro_myc.models.product import Producto
from lubricentro_myc.models.sale import Venta
from lubricentro_myc.tests.factories import ProductFactory, SaleFactory
from lubricentro_myc.utils import mock_auth
from rest_framework.test import APIClient


class SaleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()
        cls.client_url = "/lubricentro_myc/ventas"
        cls.product_1 = ProductFactory(codigo=1, stock=5)
        cls.product_2 = ProductFactory(codigo=2, stock=4)
        cls.sale_1 = {
            "producto": cls.product_1.codigo,
            "cantidad": 3,
            "precio": "700",
        }
        cls.sale_2 = {
            "producto": cls.product_2.codigo,
            "cantidad": 1,
            "precio": "1500",
        }

    @mock_auth
    def test_get_sales_by_date(self):
        sale_1 = SaleFactory(fecha="2020-01-12")
        sale_2 = SaleFactory(fecha="2020-03-05")
        sale_3 = SaleFactory(fecha="2021-03-15")
        sale_4 = SaleFactory(fecha="2021-03-25")
        cases = (
            {
                "case_name": "Should return sales made in 2020-01-12",
                "query_params": "?dia=12&mes=01&anio=2020",
                "expected_result": [sale_1.id],
            },
            {
                "case_name": "Should return sales made in 2020",
                "query_params": "?anio=2020",
                "expected_result": [sale_1.id, sale_2.id],
            },
            {
                "case_name": "Should return sales made in March 2021",
                "query_params": "?mes=03&anio=2021",
                "expected_result": [sale_3.id, sale_4.id],
            },
        )
        for case in cases:
            with self.subTest(msg=case["case_name"]):
                response = self.client.get(
                    f"{self.client_url}{case['query_params']}",
                    follow=True,
                )
                self.assertEqual(
                    list(map(lambda x: x["id"], response.data["results"])),
                    case["expected_result"],
                )

    @mock_auth
    def test_new_sale_without_updating_stock(self):
        self.client.post(
            f"{self.client_url}/",
            json.dumps(self.sale_1),
            content_type="application/json",
            follow=True,
        )
        self.client.post(
            f"{self.client_url}/",
            json.dumps(self.sale_2),
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

    @mock_auth
    def test_new_sale_updating_stock(self):
        self.client.post(
            f"{self.client_url}/?update_stock=true",
            json.dumps(self.sale_1),
            content_type="application/json",
            follow=True,
        )
        self.client.post(
            f"{self.client_url}/?update_stock=true",
            json.dumps(self.sale_2),
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

    @mock_auth
    def test_bulk_sale(self):
        sales = [self.sale_1, self.sale_2]
        self.client.post(
            f"{self.client_url}/bulk/?update_stock=true",
            json.dumps({"ventas": sales}),
            content_type="application/json",
            follow=True,
        )
        sales = Venta.objects.all()
        self.assertEqual(len(sales), 2)

    @mock_auth
    def test_sales_per_year(self):
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

    @mock_auth
    def test_sales_per_month(self):
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
