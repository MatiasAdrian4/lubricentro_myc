from dateutil import parser
from django.test import TestCase
from rest_framework.test import APIClient

from lubricentro_myc.models.account_summary_item import DEBE, HABER
from lubricentro_myc.tests.factories import ClientFactory, AccountSummaryItemFactory
from lubricentro_myc.utils import mock_auth


class AccountSummaryItemTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()
        cls.client_url = "/lubricentro_myc/account_summaries"

        client_1 = ClientFactory(id=10, nombre="Carlos")
        client_2 = ClientFactory(id=11, nombre="Pedro")

        cls.account_summary_item_1 = AccountSummaryItemFactory(
            id=1,
            client=client_1,
            date=parser.parse("2024-01-15"),
            description="test 1",
            type=DEBE,
            amount=35200,
        )
        cls.account_summary_item_2 = AccountSummaryItemFactory(
            id=2,
            client=client_1,
            date=parser.parse("2024-03-21"),
            description="test 2",
            type=HABER,
            amount=25105,
        )
        cls.account_summary_item_3 = AccountSummaryItemFactory(
            id=3,
            client=client_2,
            date=parser.parse("2024-06-10"),
            description="test 3",
            type=DEBE,
            amount=21789.25,
        )
        cls.account_summary_item_4 = AccountSummaryItemFactory(
            id=4,
            client=client_1,
            date=parser.parse("2024-08-03"),
            description="test 4",
            type=HABER,
            amount=1300,
        )
        cls.account_summary_item_5 = AccountSummaryItemFactory(
            id=5,
            client=client_1,
            date=parser.parse("2024-11-04"),
            description="test 5",
            type=DEBE,
            amount=15240.25,
        )
        cls.account_summary_item_6 = AccountSummaryItemFactory(
            id=6,
            client=client_1,
            date=parser.parse("2025-01-02"),
            description="test 6",
            type=HABER,
            amount=3450,
        )

    @mock_auth
    def test_account_summary_items_for_client_in_a_date_range(self):
        response = self.client.get(
            f"{self.client_url}?client_id=10&start_date=2024-01-01&end_date=2024-12-31",
            follow=True,
        )
        account_summary_items = response.data
        self.assertEqual(len(account_summary_items), 4)
        self.assertEqual(account_summary_items[0]["id"], self.account_summary_item_1.id)
        self.assertEqual(account_summary_items[1]["id"], self.account_summary_item_2.id)
        self.assertEqual(account_summary_items[2]["id"], self.account_summary_item_4.id)
        self.assertEqual(account_summary_items[3]["id"], self.account_summary_item_5.id)
