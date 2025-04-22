import socket
import unittest

from django.conf import settings

from ..session import WialonSession


class WialonSessionTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.session = WialonSession()

    def test_session_init(self) -> None:
        self.assertEqual(self.session.token, settings.WIALON_TOKEN)
        self.assertIsNone(self.session.id)
        self.assertIsNone(self.session.username)
        self.assertIsNone(self.session.uid)

    def test_session_login(self) -> None:
        mock_login_response = {"host": socket.gethostbyname(socket.gethostname())}

        self.session.login(settings.WIALON_TOKEN)
