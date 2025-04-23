from authorizenet import apicontractsv1, apicontrollers
from authorizenet.apicontrollersbase import APIOperationBase
from django import forms

from .auth import get_environment, get_merchant_auth
from .errors import ControllerExecutionError


class ControllerExecutionMixin:
    @staticmethod
    def execute_controller(controller: APIOperationBase) -> dict | None:
        """
        Executes an Authorizenet controller and returns its response.

        :param controller: An Authorizenet API controller.
        :type controller: :py:obj:`~authorizenet.apicontrollersbase.APIOperationBase`
        :raises ControllerExecutionError: If the API call fails.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        controller.setenvironment(get_environment())
        controller.execute()
        response = controller.getresponse()

        if response is not None and response.messages.resultCode != "Ok":
            raise ControllerExecutionError(
                message=response.messages.message[0]["text"].text,
                code=response.messages.message[0]["code"].text,
            )
        return response


def get_customer_profile_ids() -> list[int]:
    """
    Returns a list of all customer profile ids in Authorizenet.

    :raises ControllerExecutionError: If the API call fails.
    :returns: A list of all customer profile ids in Authorizenet.
    :rtype: :py:obj:`list`

    """
    request = apicontractsv1.getCustomerProfileIdsRequest(
        merchantAuthentication=get_merchant_auth()
    )
    controller = apicontrollers.getCustomerProfileIdsController(request)
    controller.setenvironment(get_environment())
    controller.execute()
    response = controller.getresponse()

    if response is not None and response.messages.resultCode != "Ok":
        raise ControllerExecutionError(
            message=response.messages.message[0]["text"].text,
            code=response.messages.message[0]["code"].text,
        )
    return [int(id) for id in response.ids.getchildren()]


def get_customer_profile_id(email: str) -> int | None:
    """
    Retrieves an Authorizenet customer profile id by email address.

    :param email: A customer email address.
    :type email: :py:obj:`str`
    :raises ControllerExecutionError: If something goes wrong with the Authorizenet API.
    :returns: A customer profile id, if found.
    :rtype: :py:obj:`int` | :py:obj:`None`

    """
    request = apicontractsv1.getCustomerProfileRequest(
        merchantAuthentication=get_merchant_auth(), email=email, includeIssuerInfo=False
    )
    controller = apicontrollers.getCustomerProfileController(request)
    controller.setenvironment(get_environment())
    controller.execute()
    response = controller.getresponse()

    if response is not None and response.messages.resultCode != "Ok":
        raise ControllerExecutionError(
            message=response.messages.message[0]["text"].text,
            code=response.messages.message[0]["code"].text,
        )
    return int(response.profile.customerProfileId)


def generate_customer_address(form: forms.Form) -> apicontractsv1.customerAddressType:
    """Takes a form and returns a :py:obj:`~authorizenet.apicontractsv1.customerAddressType`."""
    address: apicontractsv1.customerAddressType = form.cleaned_data["address"]
    address.firstName = form.cleaned_data["first_name"]
    address.lastName = form.cleaned_data["last_name"]
    address.phone = form.cleaned_data["phone"]
    return address


def generate_customer_payment(form: forms.Form) -> apicontractsv1.paymentType:
    """Takes a form and returns a :py:obj:`~authorizenet.apicontractsv1.paymentType`."""
    credit_card = form.cleaned_data["credit_card"]
    return apicontractsv1.paymentType(creditCard=credit_card)
