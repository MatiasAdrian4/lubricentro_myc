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
        cls.client_1 = ClientFactory(id=1, nombre="Jose Gomez")
        cls.client_2 = ClientFactory(id=15, nombre="Juan Perez")
        cls.client_3 = ClientFactory(id=30, nombre="Maria Fernandez")
        cls.client_4 = ClientFactory(id=45, nombre="Jose Hernandez")

    @mock_auth
    def test_search_client(self):
        response = self.client.get(f"{self.client_url}?nombre=jose", follow=True)
        clientes = json.loads(response.content)["results"]
        self.assertEqual(len(clientes), 2)
        self.assertEqual(clientes[0]["nombre"], "Jose Gomez")
        self.assertEqual(clientes[1]["nombre"], "Jose Hernandez")

    @mock_auth
    def test_search_client_using_query_param_to_search_by_id(self):
        response = self.client.get(f"{self.client_url}?query=1", follow=True)
        clientes = json.loads(response.content)["results"]
        self.assertEqual(len(clientes), 2)
        self.assertEqual(clientes[0]["id"], 1)
        self.assertEqual(clientes[1]["id"], 15)

    @mock_auth
    def test_search_client_using_query_param_to_search_by_name(self):
        response = self.client.get(f"{self.client_url}?query=jose", follow=True)
        clientes = json.loads(response.content)["results"]
        self.assertEqual(len(clientes), 2)
        self.assertEqual(clientes[0]["nombre"], "Jose Gomez")
        self.assertEqual(clientes[1]["nombre"], "Jose Hernandez")
