from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

if not hasattr(settings, "DEBUG"):
    raise ImproperlyConfigured("'DEBUG' setting is required.")
if not hasattr(settings, "MERCHANT_AUTH_LOGIN_ID"):
    raise ImproperlyConfigured("'MERCHANT_AUTH_LOGIN_ID' setting is required.")
if not hasattr(settings, "MERCHANT_AUTH_TRANSACTION_KEY"):
    raise ImproperlyConfigured("'MERCHANT_AUTH_TRANSACTION_KEY' setting is required.")
