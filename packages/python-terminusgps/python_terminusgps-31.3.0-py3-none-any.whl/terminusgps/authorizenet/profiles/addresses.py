from authorizenet import apicontractsv1, apicontrollers

from .base import AuthorizenetSubProfileBase


class AddressProfile(AuthorizenetSubProfileBase):
    """An Authorizenet customer address profile."""

    def create(self, address: apicontractsv1.customerAddressType) -> int:
        """
        Creates an Authorizenet address profile.

        :param address: A customer address.
        :type address: :py:obj:`~authorizenet.apicontractsv1.customerAddressType`
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :raises ValueError: If the Authorizenet API response was not retrieved.
        :returns: A new address profile id.
        :rtype: :py:obj:`int`

        """
        response = self._authorizenet_create_shipping_address(address)
        if response is None:
            raise ValueError("Failed to retrieve Authorizenet API response.")
        return int(response.customerAddressId)

    def update(self, address: apicontractsv1.customerAddressType) -> dict | None:
        """
        Updates the Authorizenet address profile.

        :param address: A customer shipping address.
        :type address: :py:obj:`~authorizenet.apicontractsv1.customerAddressType`
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        return self._authorizenet_update_shipping_address(address)

    def delete(self) -> dict | None:
        """
        Deletes the Authorizenet address profile.

        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        return self._authorizenet_delete_shipping_address()

    def get_details(self) -> dict | None:
        """
        Gets details for the Authorizenet address profile.

        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        return self._authorizenet_get_shipping_address()

    def _authorizenet_get_shipping_address(self) -> dict | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.getCustomerShippingAddressRequest` using the Authorizenet API.

        `getCustomerShippingAddressRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-get-customer-shipping-address>`_

        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        assert self.id, "'id' was not set."

        request = apicontractsv1.getCustomerShippingAddressRequest(
            merchantAuthentication=self.merchantAuthentication,
            customerProfileId=self.customerProfileId,
            customerAddressId=self.id,
        )
        controller = apicontrollers.getCustomerShippingAddressController(request)
        return self.execute_controller(controller)

    def _authorizenet_create_shipping_address(
        self, address: apicontractsv1.customerAddressType
    ) -> dict | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.createCustomerShippingAddressRequest` using the Authorizenet API.

        `createCustomerShippingAddressRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-create-customer-shipping-address>`_

        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        request = apicontractsv1.createCustomerShippingAddressRequest(
            merchantAuthentication=self.merchantAuthentication,
            customerProfileId=self.customerProfileId,
            address=address,
            defaultShippingAddress=self.default,
        )
        controller = apicontrollers.createCustomerShippingAddressController(request)
        return self.execute_controller(controller)

    def _authorizenet_update_shipping_address(
        self, address: apicontractsv1.customerAddressType
    ) -> dict | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.updateCustomerShippingAddressRequest` using the Authorizenet API.

        `updateCustomerShippingAddressRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-update-customer-shipping-address>`_

        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        assert self.id, "'id' was not set."

        address.customerAddressId = self.id
        request = apicontractsv1.updateCustomerShippingAddressRequest(
            merchantAuthentication=self.merchantAuthentication,
            customerProfileId=self.customerProfileId,
            address=address,
            default=self.default,
        )
        controller = apicontrollers.updateCustomerShippingAddressController(request)
        return self.execute_controller(controller)

    def _authorizenet_delete_shipping_address(self) -> dict | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.deleteCustomerShippingAddressRequest` using the Authorizenet API.

        `deleteCustomerShippingAddressRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-delete-customer-shipping-address>`_

        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises ControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        assert self.id, "'id' was not set."

        request = apicontractsv1.deleteCustomerShippingAddressRequest(
            merchantAuthentication=self.merchantAuthentication,
            customerProfileId=self.customerProfileId,
            customerAddressId=self.id,
        )
        controller = apicontrollers.deleteCustomerShippingAddressController(request)
        return self.execute_controller(controller)
