class ControllerExecutionError(Exception):
    """Raised when an Authorizenet API controller fails to execute."""

    def __init__(self, message: str, code: str, *args, **kwargs) -> None:
        """
        Sets :py:attr:`message` and :py:attr`code` for the exception.

        :param message: An Authorizenet API error message.
        :type message: :py:obj:`str`
        :param code: An Authorizenet API error code.
        :type code: :py:obj:`str`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        super().__init__(message, *args, **kwargs)
        self._message = message
        self._code = code

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"

    @property
    def message(self) -> str:
        """An Authorizenet API error message."""
        return self._message

    @property
    def code(self) -> str:
        """An Authorizenet API error code."""
        return self._code
