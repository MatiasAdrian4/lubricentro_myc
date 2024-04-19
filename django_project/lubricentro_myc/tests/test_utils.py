from django.test import TestCase

from lubricentro_myc.utils import round_up_price


class UtilsTestCase(TestCase):
    def test_round_up_price(self):
        self.assertEqual(round_up_price(15), 15.0)
        self.assertEqual(round_up_price(15.55), 16.0)
        self.assertEqual(round_up_price(15.05), 16.0)
        self.assertEqual(round_up_price(15.3333333), 16.0)
