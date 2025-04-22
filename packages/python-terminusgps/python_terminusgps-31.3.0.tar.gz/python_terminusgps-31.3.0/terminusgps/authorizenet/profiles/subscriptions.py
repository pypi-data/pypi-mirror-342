import decimal

from authorizenet import apicontractsv1, apicontrollers

from ..auth import get_merchant_auth
from ..utils import ControllerExecutionMixin


class SubscriptionProfile(ControllerExecutionMixin):
    """An Authorizenet subscription profile."""

    def __init__(self, id: str | int | None = None, *args, **kwargs) -> None:
        if id and isinstance(id, str) and not id.isdigit():
            raise ValueError(f"'id' must be a digit, got '{id}'.")
        self.id = int(id) if id else self.create(*args, **kwargs)

    def create(
        self,
        name: str,
        amount: decimal.Decimal,
        schedule: apicontractsv1.paymentScheduleType,
        profile_id: int | str,
        payment_id: int | str,
        address_id: int | str,
        trial_amount: decimal.Decimal = decimal.Decimal(
            0.00, context=decimal.Context(prec=2, rounding=decimal.ROUND_HALF_UP)
        ),
    ) -> int:
        """
        Creates a subscription in Authorizenet.

        :param name: A name for the subscription.
        :type name: :py:obj:`str`
        :param amount: An amount of money paid per occurrence of the subscription.
        :type amount: :py:obj:`~decimal.Decimal`
        :param schedule: A payment schedule for the subscription.
        :type amount: :py:obj:`~authorizenet.apicontractsv1.paymentScheduleType`
        :param profile_id: An Authorizenet customer profile id.
        :type profile_id: :py:obj:`int` | :py:obj:`str`
        :param payment_id: An Authorizenet customer payment profile id.
        :type payment_id: :py:obj:`int` | :py:obj:`str`
        :param address_id: An Authorizenet customer address profile id.
        :type address_id: :py:obj:`int` | :py:obj:`str`
        :param trial_amount: Trial amount for the subscription. Default is ``0.00``.
        :type trial_amount: :py:obj:`~decimal.Decimal`
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :raises ValueError: If ``profile_id`` wasn't a digit.
        :raises ValueError: If ``payment_id`` wasn't a digit.
        :raises ValueError: If ``address_id`` wasn't a digit.
        :raises ValueError: If the Authorizenet API response was not retrieved.
        :returns: An Authorizenet subscription id.
        :rtype: :py:obj:`int`

        """
        if isinstance(profile_id, str) and not profile_id.isdigit():
            raise ValueError(f"'profile_id' must be a digit, got '{profile_id}'.")
        if isinstance(payment_id, str) and not payment_id.isdigit():
            raise ValueError(f"'payment_id' must be a digit, got '{payment_id}'.")
        if isinstance(address_id, str) and not address_id.isdigit():
            raise ValueError(f"'address_id' must be a digit, got '{address_id}'.")

        subscription: apicontractsv1.ARBSubscriptionType = (
            apicontractsv1.ARBSubscriptionType(
                name=name,
                paymentSchedule=schedule,
                amount=amount,
                trialAmount=trial_amount,
                profile=apicontractsv1.customerProfileIdType(
                    customerProfileId=str(profile_id),
                    customerPaymentProfileId=str(payment_id),
                    customerAddressId=str(address_id),
                ),
            )
        )
        response = self._authorizenet_create_subscription(subscription)
        if response is None:
            raise ValueError("Failed to retrieve Authorizenet API response.")
        return int(response.subscriptionId)

    def cancel(self) -> None:
        """
        Cancels the subscription.

        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self._authorizenet_cancel_subscription()

    def update(self, subscription: apicontractsv1.ARBSubscriptionType) -> None:
        """
        Updates a subscription in Authorizenet.

        :param subscription: A new subscription object.
        :type subscription: :py:obj:`authorizenet.apicontractsv1.ARBSubscriptionType`
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self._authorizenet_update_subscription(subscription)

    @property
    def merchantAuthentication(self) -> apicontractsv1.merchantAuthenticationType:
        """Merchant authentication for API calls."""
        return get_merchant_auth()

    @property
    def status(self) -> str | None:
        """Current status of the subscription."""
        if not self.id:
            return

        response = self._authorizenet_get_subscription_status()
        if response is not None and "status" in response.__dir__():
            return response.status

    @property
    def transactions(self) -> list | None:
        """Transactions for the subscription."""
        if not self.id:
            return

        response = self._authorizenet_get_subscription(include_transactions=True)
        return [t for t in response.subscription.arbTransactions.iterchildren()]

    @property
    def payment_id(self) -> int | None:
        """Customer payment profile id for the subscription."""
        if not self.id:
            return

        response = self._authorizenet_get_subscription()
        if response is not None and "profile" in response.getchildren():
            return int(response.profile.paymentProfile.customerPaymentProfileId)

    @property
    def address_id(self) -> int | None:
        """Customer address profile id for the subscription."""
        if not self.id:
            return

        response = self._authorizenet_get_subscription()
        if response is not None and "profile" in response.getchildren():
            return int(response.profile.shippingProfile.customerAddressId)

    def _authorizenet_create_subscription(
        self, subscription: apicontractsv1.ARBSubscriptionType
    ) -> dict | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.ARBCreateSubscriptionRequest` using the Authorizenet API.

        `ARBCreateSubscriptionRequest <https://developer.authorize.net/api/reference/index.html#recurring-billing-create-a-subscription-from-customer-profile>`_

        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        request = apicontractsv1.ARBCreateSubscriptionRequest(
            merchantAuthentication=self.merchantAuthentication,
            subscription=subscription,
        )
        controller = apicontrollers.ARBCreateSubscriptionController(request)
        return self.execute_controller(controller)

    def _authorizenet_get_subscription(
        self, include_transactions: bool = False
    ) -> dict | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.ARBGetSubscriptionRequest` using the Authorizenet API.

        `ARBGetSubscriptionRequest <https://developer.authorize.net/api/reference/index.html#recurring-billing-get-subscription>`_

        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        assert self.id, "'id' was not set."

        request = apicontractsv1.ARBGetSubscriptionRequest(
            merchantAuthentication=self.merchantAuthentication,
            subscriptionId=str(self.id),
            includeTransactions=str(include_transactions).lower(),
        )
        controller = apicontrollers.ARBGetSubscriptionController(request)
        return self.execute_controller(controller)

    def _authorizenet_get_subscription_status(self) -> dict | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.ARBGetSubscriptionStatusRequest` using the Authorizenet API.

        `ARBGetSubscriptionStatusRequest <https://developer.authorize.net/api/reference/index.html#recurring-billing-get-subscription-status>`_

        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        assert self.id, "'id' was not set."

        request = apicontractsv1.ARBGetSubscriptionStatusRequest(
            merchantAuthentication=self.merchantAuthentication,
            subscriptionId=str(self.id),
        )
        controller = apicontrollers.ARBGetSubscriptionStatusController(request)
        return self.execute_controller(controller)

    def _authorizenet_update_subscription(
        self, subscription: apicontractsv1.ARBSubscriptionType
    ) -> dict | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.ARBUpdateSubscriptionRequest` using the Authorizenet API.

        `ARBUpdateSubscriptionRequest <https://developer.authorize.net/api/reference/index.html#recurring-billing-update-a-subscription>`_

        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        assert self.id, "'id' was not set."

        request = apicontractsv1.ARBUpdateSubscriptionRequest(
            merchantAuthentication=self.merchantAuthentication,
            subscriptionId=str(self.id),
            subscription=subscription,
        )
        controller = apicontrollers.ARBUpdateSubscriptionController(request)
        return self.execute_controller(controller)

    def _authorizenet_cancel_subscription(self) -> dict | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.ARBCancelSubscriptionRequest` using the Authorizenet API.

        `ARBCancelSubscriptionRequest <https://developer.authorize.net/api/reference/index.html#recurring-billing-cancel-a-subscription>`_

        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        assert self.id, "'id' was not set."

        request = apicontractsv1.ARBCancelSubscriptionRequest(
            merchantAuthentication=self.merchantAuthentication,
            subscriptionId=str(self.id),
        )
        controller = apicontrollers.ARBCancelSubscriptionController(request)
        return self.execute_controller(controller)
