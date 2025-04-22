import unittest

from django.conf import settings

from ..session import WialonSession


class WialonSessionTestCase(unittest.TestCase):
    def setUp(self) -> None:
        if not hasattr(settings, "WIALON_TOKEN"):
            self.fail("'WIALON_TOKEN' setting is required.")

        self.token = settings.WIALON_TOKEN
        self.session = WialonSession()

    def test_session_init(self) -> None:
        self.assertIsNone(self.session.id)
        self.assertIsNone(self.session.username)
        self.assertIsNone(self.session.uid)

    def test_session_login(self) -> None:
        sid: str = self.session.login(self.token)
        self.assertEqual(self.session.id, sid)

    def test_session_logout(self) -> None:
        self.session.login(self.token)
        self.session.logout()
        self.assertEqual(self.session.id, None)

    def test_session_bad_call(self) -> None:
        self.session.login(self.token)
        response = self.session.wialon_api.core_bad_call({})
        self.assertEqual(response, None)
        self.session.logout()

    def test_session_valid_call_count(self) -> None:
        self.session.login(self.token)  # Login/logout does not count
        self.session.wialon_api.avl_evts()
        self.assertEqual(self.session.wialon_api.total_calls, 1)
        self.session.logout()
