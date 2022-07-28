import json

from django.test import TestCase
from lubricentro_myc.models.product import Producto
from lubricentro_myc.tests.factories import ProductFactory
from lubricentro_myc.utils import mock_auth
from rest_framework.test import APIClient


class ProductTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()
        cls.client_url = "/lubricentro_myc/productos"
        cls.product_1 = ProductFactory(
            codigo=1,
            codigo_en_pantalla=1,
            detalle="CORREA GATES 5PK1815-9",
            categoria="Correas",
            precio_costo=2025.00,
        )
        cls.product_2 = ProductFactory(
            codigo=2,
            codigo_en_pantalla=2,
            detalle="CABLE BUJIA R-12 81 EN ADEL.( 26253-R)",
            categoria="Electricidad",
            precio_costo=133.0,
        )
        cls.product_3 = ProductFactory(
            codigo=3,
            codigo_en_pantalla=3,
            detalle="KIT DISTRIBUCION AMAROK (SKF)",
            categoria="Correas",
            precio_costo=25146.0,
        )
        cls.product_4 = ProductFactory(
            codigo=4,
            codigo_en_pantalla=4,
            detalle="CORREA BTS 13X660",
            categoria="Correas",
            precio_costo=514.0,
        )
        cls.product_5 = ProductFactory(
            codigo=5,
            codigo_en_pantalla=5,
            detalle="DESTELLADOR ELEC.12V ALTERNATIVO Nº 78",
            categoria="Electricidad",
            precio_costo=1157.0,
        )
        cls.product_6 = ProductFactory(
            codigo=6,
            codigo_en_pantalla=6,
            detalle="FICHA 5T.M-BENZ/FORD CARGO",
            categoria="Electricidad",
            precio_costo=147.0,
        )

    @mock_auth
    def test_search_by_detail(self):
        response = self.client.get(f"{self.client_url}?detalle=correa", follow=True)
        productos = json.loads(response.content)["results"]
        self.assertEqual(len(productos), 2)
        self.assertEqual(productos[0]["codigo"], self.product_1.codigo)
        self.assertEqual(productos[1]["codigo"], self.product_4.codigo)

    @mock_auth
    def test_search_by_category(self):
        response = self.client.get(
            f"{self.client_url}?categoria=electricidad",
            follow=True,
        )
        productos = json.loads(response.content)["results"]
        self.assertEqual(len(productos), 3)
        self.assertEqual(productos[0]["codigo"], self.product_2.codigo)
        self.assertEqual(productos[1]["codigo"], self.product_5.codigo)
        self.assertEqual(productos[2]["codigo"], self.product_6.codigo)

    @mock_auth
    def test_search_by_query(self):
        product_7 = ProductFactory(
            codigo=7,
            codigo_en_pantalla=41,
            detalle="FILTRO CHATO T.AGUA PERKINS [PB-212)",
            categoria="Filtros",
            precio_costo=45.72,
        )

        cases = (
            {
                "case_name": "Should return products with categories matching 'corr'",
                "query_params": "?query=corr",
                "expected_result": [
                    self.product_1.codigo,
                    self.product_3.codigo,
                    self.product_4.codigo,
                ],
            },
            {
                "case_name": "Should return products with detail matching 'fi'",
                "query_params": "?query=fi",
                "expected_result": [self.product_6.codigo, product_7.codigo],
            },
            {
                "case_name": "Should return products with code matching '4'",
                "query_params": "?query=4",
                "expected_result": [self.product_4.codigo, product_7.codigo],
            },
        )

        for case in cases:
            with self.subTest(msg=case["case_name"]):
                response = self.client.get(
                    f"{self.client_url}{case['query_params']}",
                    follow=True,
                )
                self.assertEqual(
                    list(map(lambda x: x["codigo"], response.data["results"])),
                    case["expected_result"],
                )

    @mock_auth
    def test_update_products_cost(self):
        response = self.client.post(
            f"{self.client_url}/aumento_masivo_precio_costo/",
            json.dumps(
                {"porcentaje_aumento": 25, "productos": [1, 2, 3, 4, 5, 6, 999999]}
            ),
            content_type="application/json",
            follow=True,
        )
        resultado = json.loads(response.content)["resultado"]
        productos = Producto.objects.all()
        self.assertEqual(resultado, "6 producto/s actualizado/s satisfactoriamente.")
        self.assertEqual(productos[0].precio_costo, 2531.25)
        self.assertEqual(productos[1].precio_costo, 166.25)
        self.assertEqual(productos[2].precio_costo, 31432.5)
        self.assertEqual(productos[3].precio_costo, 642.5)
        self.assertEqual(productos[4].precio_costo, 1446.25)
        self.assertEqual(productos[5].precio_costo, 183.75)
