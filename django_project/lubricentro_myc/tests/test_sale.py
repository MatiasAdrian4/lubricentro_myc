import json
from unittest.mock import MagicMock, patch

from django.test import TestCase
from lubricentro_myc.models import Venta
from lubricentro_myc.tests.factories import ProductFactory
from rest_framework.test import APIClient


class SaleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()
        cls.client_url = "/lubricentro_myc/ventas_realizadas"
        cls.product_1 = ProductFactory(codigo=1)
        cls.product_2 = ProductFactory(codigo=2)

    @patch("lubricentro_myc.authentication.JWTAuthentication.authenticate")
    def test_new_sale(self, mock_auth):
        mock_auth.return_value = (MagicMock(), None)
        self.client.post(
            f"{self.client_url}/guardar_venta/",
            json.dumps(
                {
                    "ventas": [
                        {
                            "producto": self.product_1.codigo,
                            "cantidad": 3,
                            "precio": "700",
                        },
                        {
                            "producto": self.product_2.codigo,
                            "cantidad": 1,
                            "precio": "1500",
                        },
                    ]
                }
            ),
            content_type="application/json",
            follow=True,
        )
        sales = Venta.objects.all()
        self.assertEqual(len(sales), 2)
        self.assertEqual(sales[0].producto.codigo, self.product_1.codigo)
        self.assertEqual(sales[1].producto.codigo, self.product_2.codigo)
