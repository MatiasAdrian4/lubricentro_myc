from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

import logging

logger = logging.getLogger("django")


class Command(BaseCommand):
    help = "Stores mock data in the DB"

    def store_mock_users(self):
        try:
            User.objects.get(username="test_user")
            logger.info("0 users were created.")
        except User.DoesNotExist:
            User.objects.create_user(
                username="test_user", email="", password="test_password"
            )
            logger.info("1 user was created.")

    def store_mock_products(self):
        logger.info("0 products were created.")

    def store_mock_clients(self):
        logger.info("0 clients were created.")

    def handle(self, *args, **kwargs):
        logger.info("Creating test data...")
        self.store_mock_users()
        self.store_mock_products()
        self.store_mock_clients()
        logger.info("Finished.")