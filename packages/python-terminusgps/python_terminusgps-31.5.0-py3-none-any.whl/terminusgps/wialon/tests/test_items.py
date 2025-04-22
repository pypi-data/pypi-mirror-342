import unittest
from datetime import datetime

from django.conf import settings

from .. import items
from ..session import WialonSession


class WialonResourceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        if not hasattr(settings, "WIALON_TOKEN"):
            self.fail("'WIALON_TOKEN' setting is required.")
        if not hasattr(settings, "WIALON_ADMIN_ID"):
            self.fail("'WIALON_ADMIN_ID' setting is required.")

        self.session = WialonSession()
        self.session.login(settings.WIALON_TOKEN)
        self.test_timestamp = f"{datetime.now():%Y-%m-%d-%H:%M:%S}"
        self.test_resource = items.WialonResource(
            id=None,
            creator_id=str(settings.WIALON_ADMIN_ID),
            name=f"test_resource_{self.test_timestamp}",
            skip_creator_check=True,
            session=self.session,
        )

    def tearDown(self) -> None:
        self.test_resource.delete()

    def test_resource_is_not_account(self) -> None:
        """Tests whether or not a new resource is an account after creation."""
        self.assertFalse(self.test_resource.is_account)

    def test_resource_create_account(self) -> None:
        self.test_resource.create_account("terminusgps_ext_hist")
        self.assertTrue(self.test_resource.is_account)
