import unittest

import batch_player_upgrade as bpu


class TestGetClientId(unittest.TestCase):
    def test_get_client_id_returns_placeholder_value(self):
        assert bpu.get_client_id() == "dummy_client_id"


if __name__ == '__main__':
    unittest.main()
