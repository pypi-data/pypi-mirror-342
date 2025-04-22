import uuid
from datetime import datetime
from unittest import TestCase

from terminusgps.authorizenet.auth import get_merchant_auth
from terminusgps.authorizenet.profiles import CustomerProfile


class CustomerProfileTestCase(TestCase):
    def setUp(self) -> None:
        self.merchantAuthentication = get_merchant_auth()
        self.test_timestamp = f"{datetime.now():%Y-%m-%d-%H:%M:%S}"
        self.test_id = str(uuid.uuid4())[:24]
        self.test_email = f"test_customer_{self.test_id}@domain.com"
        self.test_desc = f"Test customer created on: {self.test_timestamp}"
        self.test_customer_profile = CustomerProfile(
            merchant_id=self.test_id,
            id=None,
            email=self.test_email,
            desc=self.test_desc,
        )

    def tearDown(self) -> None:
        self.test_customer_profile.delete()

    def test_customer_profile_update(self) -> None:
        old_email: str = self.test_email
        new_email: str = f"test_customer_{str(uuid.uuid4())[:24]}@domain.com"
        self.test_customer_profile.update(email=new_email)
        self.assertTrue(self.test_customer_profile.email, new_email)
        self.assertFalse(self.test_customer_profile.email, old_email)


class AddressProfileTestCase(TestCase):
    def setUp(self) -> None:
        self.merchantAuthentication = get_merchant_auth()
