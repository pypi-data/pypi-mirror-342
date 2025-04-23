from unittest import TestCase

import django
from django.core.exceptions import ValidationError

from terminusgps.twilio import validators

django.setup()


class PhoneNumberValidatorTestCase(TestCase):
    def setUp(self) -> None:
        self.validator = validators.validate_phone_number

    def test_phone_without_plus(self) -> None:
        """Fails if a phone number without a '+' leading character passes validation."""
        with self.assertRaises(ValidationError) as context:
            self.validator("15555555555")
        self.assertTrue(
            "Phone number must begin with a '+', got '15555555555'."
            in str(context.exception)
        )

    def test_phone_min_length(self) -> None:
        """Fails if a phone number of 8 characters in length passes validation."""
        with self.assertRaises(ValidationError) as context:
            self.validator("+1555555")
        self.assertTrue(
            "Phone number cannot be less than 12 characters, got 8."
            in str(context.exception)
        )

    def test_phone_max_length(self) -> None:
        """Fails if a phone number of 20 characters in length passes validation."""
        with self.assertRaises(ValidationError) as context:
            self.validator("+1555555555555555555")
        self.assertTrue(
            "Phone number cannot be greater than 19 characters, got 20."
            in str(context.exception)
        )
