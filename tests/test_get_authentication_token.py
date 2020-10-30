import unittest

import batch_player_upgrade as bpu


class TestGetAuthenticationToken(unittest.TestCase):
    def test_get_authentication_token_returns_placeholder_value(self):
        assert bpu.get_authentication_token() == "dummy_authentication_token"


if __name__ == '__main__':
    unittest.main()
