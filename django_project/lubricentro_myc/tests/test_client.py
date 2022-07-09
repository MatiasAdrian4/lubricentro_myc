import json

from django.test import TestCase
from lubricentro_myc.tests.factories import ClientFactory
from lubricentro_myc.utils import mock_auth
from rest_framework.test import APIClient


class ClientTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()
        cls.client_url = "/lubricentro_myc/clientes"
        cls.client_1 = ClientFactory(nombre="Jose Gomez")
        cls.client_2 = ClientFactory(nombre="Juan Perez")
        cls.client_3 = ClientFactory(nombre="Maria Fernandez")
        cls.client_4 = ClientFactory(nombre="Jose Hernandez")

    @mock_auth
    def test_search_client(self):
        response = self.client.get(f"{self.client_url}?nombre=jose", follow=True)
        clientes = json.loads(response.content)["results"]
        self.assertEqual(len(clientes), 2)
        self.assertEqual(clientes[0]["nombre"], "Jose Gomez")
        self.assertEqual(clientes[1]["nombre"], "Jose Hernandez")
