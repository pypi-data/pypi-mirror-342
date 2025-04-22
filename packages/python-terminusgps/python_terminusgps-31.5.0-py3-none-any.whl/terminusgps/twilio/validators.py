from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone_number(value: str) -> None:
    min_length, max_length = 12, 19

    if not value.startswith("+"):
        raise ValidationError(
            _("Phone number must begin with a '+', got '%(value)s'."),
            code="invalid",
            params={"value": value},
        )
    if not value[1:].isdigit():
        raise ValidationError(
            _("Phone number must be '+' followed by a digit, got '%(value)s'"),
            code="invalid",
            params={"value": value},
        )
    if len(value) < min_length:
        raise ValidationError(
            _("Phone number cannot be less than %(min)s characters, got %(len)s."),
            code="invalid",
            params={"min": min_length, "len": len(value)},
        )
    if len(value) > max_length:
        raise ValidationError(
            _("Phone number cannot be greater than %(max)s characters, got %(len)s."),
            code="invalid",
            params={"max": max_length, "len": len(value)},
        )
