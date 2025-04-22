from authorizenet.apicontractsv1 import merchantAuthenticationType
from authorizenet.constants import constants
from django.conf import settings


def get_merchant_auth() -> merchantAuthenticationType:
    """
    Returns the merchant authentication information for Authorizenet API requests.

    :returns: A merchant authentication object.
    :rtype: :py:obj:`~authorizenet.apicontractsv1.merchantAuthenticationType`

    """
    return merchantAuthenticationType(
        name=str(settings.MERCHANT_AUTH_LOGIN_ID),
        transactionKey=str(settings.MERCHANT_AUTH_TRANSACTION_KEY),
    )


def get_environment() -> str:
    """
    Returns the environment for Authorizenet API requests.

    :returns: An Authorizenet API environment string.
    :rtype: :py:obj:`str`

    """
    return constants.SANDBOX if settings.DEBUG else constants.PRODUCTION


def get_validation_mode() -> str:
    """
    Returns the validation mode for Authorizenet API requests.

    :returns: An Authorizenet API validation string.
    :rtype: :py:obj:`str`

    """
    return "testMode" if settings.DEBUG else "liveMode"
