import json
from unittest.mock import MagicMock, patch

from django.test import TestCase
from lubricentro_myc.models.product import Producto
from lubricentro_myc.tests.factories import ProductFactory
from rest_framework.test import APIClient


class ProductTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()
        cls.client_url = "/lubricentro_myc/productos"
        cls.product_1 = ProductFactory(
            codigo=1,
            detalle="CORREA GATES 5PK1815-9",
            categoria="Correas",
            precio_costo=2025.00,
        )
        cls.product_2 = ProductFactory(
            codigo=2,
            detalle="CABLE BUJIA R-12 81 EN ADEL.( 26253-R)",
            categoria="Electricidad",
            precio_costo=133.0,
        )
        cls.product_3 = ProductFactory(
            codigo=3,
            detalle="KIT DISTRIBUCION AMAROK (SKF)",
            categoria="Correas",
            precio_costo=25146.0,
        )
        cls.product_4 = ProductFactory(
            codigo=4,
            detalle="CORREA BTS 13X660",
            categoria="Correas",
            precio_costo=514.0,
        )
        cls.product_5 = ProductFactory(
            codigo=5,
            detalle="DESTELLADOR ELEC.12V ALTERNATIVO Nº 78",
            categoria="Electricidad",
            precio_costo=1157.0,
        )
        cls.product_6 = ProductFactory(
            codigo=6,
            detalle="FICHA 5T.M-BENZ/FORD CARGO",
            categoria="Electricidad",
            precio_costo=147.0,
        )

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_search_by_detail(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)
        response = self.client.get(
            f"{self.client_url}?detalle=correa", follow=True
        )
        productos = json.loads(response.content)["results"]
        self.assertEqual(len(productos), 2)
        self.assertEqual(productos[0]["codigo"], self.product_1.codigo)
        self.assertEqual(productos[1]["codigo"], self.product_4.codigo)

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_search_by_category(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)
        response = self.client.get(
            f"{self.client_url}?categoria=electricidad",
            follow=True,
        )
        productos = json.loads(response.content)["results"]
        self.assertEqual(len(productos), 3)
        self.assertEqual(productos[0]["codigo"], self.product_2.codigo)
        self.assertEqual(productos[1]["codigo"], self.product_5.codigo)
        self.assertEqual(productos[2]["codigo"], self.product_6.codigo)

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_update_products_cost(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)
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
