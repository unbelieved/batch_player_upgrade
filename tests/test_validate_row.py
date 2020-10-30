import unittest

import batch_player_upgrade as bpu


class TestValidateRow(unittest.TestCase):

    def test_return_false_when_row_is_empty(self):
        assert bpu.validate_row([]) is False

    def test_return_false_when_first_column_is_not_a_valid_MAC_address(self):
        assert bpu.validate_row(['aa:bb:cc:dd:ee:zz']) is False
        assert bpu.validate_row(['aa:bb:cc:dd:ee:ff:aa']) is False
        assert bpu.validate_row(['aa:bb:cc:dd:ee:']) is False
        assert bpu.validate_row(['aa:bb:cc:dd:ee:f:']) is False
        assert bpu.validate_row(['potato', 'aa:bb:cc:dd:ee:ff']) is False
        assert bpu.validate_row(['', 'aa:bb:cc:dd:ee:ff']) is False

    def test_return_true_when_first_column_is_a_valid_MAC_address(self):
        assert bpu.validate_row(['aa:bb:cc:dd:ee:ff']) is True
        assert bpu.validate_row(['aa:22:CC:33:ee:00']) is True


if __name__ == '__main__':
    unittest.main()
