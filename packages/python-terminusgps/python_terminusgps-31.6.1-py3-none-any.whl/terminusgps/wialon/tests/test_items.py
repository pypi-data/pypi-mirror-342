import unittest
from datetime import datetime

from django.conf import settings

from .. import items
from ..session import WialonSession


class WialonResourceTestCase(unittest.TestCase):
    def setUp(self) -> None:
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


class WialonUnitTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.session = WialonSession()
        self.session.login(settings.WIALON_TOKEN)
        self.test_timestamp = f"{datetime.now():%Y-%m-%d-%H:%M:%S}"
        self.test_unit = items.WialonUnit(
            id=None,
            creator_id=settings.WIALON_ADMIN_ID,
            name=f"test_unit_{self.test_timestamp}",
        )
