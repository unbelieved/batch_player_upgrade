import builtins
import json
import unittest
from io import StringIO
from unittest.mock import patch

import batch_player_upgrade as bpu


class TestProcessCsv(unittest.TestCase):
    @patch("csv.reader")
    def test_process_csv_csv_reader_is_called_with_file_contents(self, mock_csv_reader):
        with patch.object(builtins, 'open') as mock_file:
            mock_file.return_value = StringIO("csv file contents\n")
            bpu.process_csv('test.csv', "client_id", [], "token")
        mock_csv_reader.assert_called_with(mock_file.return_value)

    @patch("batch_player_upgrade.validate_row")
    def test_process_csv_validation_is_called_on_every_row(self, mock_row_validator):
        mock_row_validator.return_value = False
        with patch.object(builtins, 'open') as mock_file:
            mock_file.return_value = StringIO(
                "row1\n"
                "row2\n"
                "row3\n"
                "row4\n"
                "row5\n"
            )
            bpu.process_csv('test.csv', "client_id", [], "token")
        self.assertEqual(5, mock_row_validator.call_count)
        mock_row_validator.has_call(["row1"])

    @patch("batch_player_upgrade.update_player_profile")
    @patch("batch_player_upgrade.validate_row")
    @patch("sys.stdout", new_callable=StringIO)
    def test_process_csv_validation_error_is_output_for_rows_in_error(self,
                                                                      mock_output,
                                                                      mock_row_validator,
                                                                      mock_update_player_profile):
        mock_update_player_profile.return_value.status = 200
        mock_row_validator.side_effect = [True, True, False, True, True]
        with patch.object(builtins, 'open') as mock_file:
            mock_file.return_value = StringIO(
                "MAC addresses, id1, id2, id3\n"
                "a1:bb:cc:dd:ee:ff, 1, 2, 3\n"
                "a2:bb:cc:dd:ee:ff, 1, 2, 3\n"
                "a3:bb:cc:dd:ee:ff, 1, 2, 3\n"
                "a4:bb:cc:dd:ee:ff, 1, 2, 3\n"
            )
            bpu.process_csv('test.csv', "client_id", [], "token")
        self.assertEqual(5, mock_row_validator.call_count)
        self.assertEqual("Line 3: Warning: Column 1 does not contain a valid Mac Address",
                         mock_output.getvalue().strip())

    @patch("batch_player_upgrade.update_player_profile")
    @patch("batch_player_upgrade.validate_row")
    @patch("sys.stdout", new_callable=StringIO)
    def test_process_csv_validation_error_is_not_output_for_header_row(self,
                                                                       mock_output,
                                                                       mock_row_validator,
                                                                       mock_update_player_profile):
        mock_update_player_profile.return_value.status = 200
        mock_row_validator.side_effect = [False, True, False, True, True]
        with patch.object(builtins, 'open') as mock_file:
            mock_file.return_value = StringIO(
                "MAC addresses, id1, id2, id3\n"
                "a1:bb:cc:dd:ee:ff, 1, 2, 3\n"
                "a2:bb:cc:dd:ee:ff, 1, 2, 3\n"
                "a3:bb:cc:dd:ee:ff, 1, 2, 3\n"
                "a4:bb:cc:dd:ee:ff, 1, 2, 3\n"
            )
            bpu.process_csv('test.csv', "client_id", [], "token")
        self.assertEqual(5, mock_row_validator.call_count)
        self.assertEqual("Line 3: Warning: Column 1 does not contain a valid Mac Address",
                         mock_output.getvalue().strip())

    @patch("batch_player_upgrade.update_player_profile")
    @patch("batch_player_upgrade.validate_row")
    def test_process_csv_update_player_profile_called_for_every_valid_row(self,
                                                                          mock_row_validator,
                                                                          mock_update_player_profile):
        mock_row_validator.side_effect = [False, True, False, True, True]
        mock_update_player_profile.return_value.status = 200
        with patch.object(builtins, 'open') as mock_file:
            mock_file.return_value = StringIO(
                "MAC addresses, id1, id2, id3\n"
                "a1:bb:cc:dd:ee:ff, 1, 2, 3\n"
                "a2:bb:cc:dd:ee:ff, 1, 2, 3\n"
                "a3:bb:cc:dd:ee:ff, 1, 2, 3\n"
                "a4:bb:cc:dd:ee:ff, 1, 2, 3\n"
            )
            bpu.process_csv('test.csv', "client_id", [], "token")
        self.assertEqual(3, mock_update_player_profile.call_count)
        self.assertEqual(5, mock_row_validator.call_count)

    @patch("batch_player_upgrade.update_player_profile")
    @patch("batch_player_upgrade.validate_row")
    def test_process_csv_exits_if_update_player_profile_exits_on_401_not_authorized(self,
                                                                                    mock_row_validator,
                                                                                    mock_update_player_profile):
        mock_update_player_profile.return_value.status = 401
        mock_update_player_profile.return_value.body = json.dumps({ "statusCode": 401,
                                                                    "error": "Unauthorized",
                                                                    "message": "invalid clientId or token supplied"})
        mock_row_validator.return_value = [False, True, True, True, True]
        with self.assertRaises(SystemExit) as exit_context:
            with patch.object(builtins, 'open') as mock_file:
                mock_file.return_value = StringIO(
                    "MAC addresses, id1, id2, id3\n"
                    "a1:bb:cc:dd:ee:ff, 1, 2, 3\n"
                    "a2:bb:cc:dd:ee:ff, 1, 2, 3\n"
                    "a3:bb:cc:dd:ee:ff, 1, 2, 3\n"
                    "a4:bb:cc:dd:ee:ff, 1, 2, 3\n"
                )
                bpu.process_csv('test.csv', "client_id", [], "token")
        self.assertEqual("Error: Unauthorized [401]: invalid clientId or token supplied",
                         exit_context.exception.code)

    @patch("batch_player_upgrade.update_player_profile")
    @patch("batch_player_upgrade.validate_row")
    def test_process_csv_exits_if_update_player_profile_exits_on_404_not_found(self,
                                                                               mock_row_validator,
                                                                               mock_update_player_profile):
        mock_update_player_profile.return_value.status = 404
        mock_update_player_profile.return_value.body = json.dumps({ "statusCode": 404,
                                                                    "error": "Not Found",
                                                                    "message": "profile of client 823f3161ae4f4495bf0a90c00a7dfbff does not exist"})
        mock_row_validator.return_value = [False, True, True, True, True]
        with self.assertRaises(SystemExit) as exit_context:
            with patch.object(builtins, 'open') as mock_file:
                mock_file.return_value = StringIO(
                    "MAC addresses, id1, id2, id3\n"
                    "a1:bb:cc:dd:ee:ff, 1, 2, 3\n"
                    "a2:bb:cc:dd:ee:ff, 1, 2, 3\n"
                    "a3:bb:cc:dd:ee:ff, 1, 2, 3\n"
                    "a4:bb:cc:dd:ee:ff, 1, 2, 3\n"
                )
                bpu.process_csv('test.csv', "client_id", [], "token")
        self.assertEqual("Error: Not Found [404]: profile of client 823f3161ae4f4495bf0a90c00a7dfbff does not exist",
                         exit_context.exception.code)


    @patch("batch_player_upgrade.update_player_profile")
    @patch("batch_player_upgrade.validate_row")
    def test_process_csv_exits_if_update_player_profile_exits_on_409_conflict(self,
                                                                               mock_row_validator,
                                                                               mock_update_player_profile):
        mock_update_player_profile.return_value.status = 409
        mock_update_player_profile.return_value.body = json.dumps({ "statusCode": 409,
                                                                    "error": "Conflict",
                                                                    "message": "child \"profile\" fails because [child \"applications\" fails because [\"applications\" is required]]"})
        mock_row_validator.return_value = [False, True, True, True, True]
        with self.assertRaises(SystemExit) as exit_context:
            with patch.object(builtins, 'open') as mock_file:
                mock_file.return_value = StringIO(
                    "MAC addresses, id1, id2, id3\n"
                    "a1:bb:cc:dd:ee:ff, 1, 2, 3\n"
                    "a2:bb:cc:dd:ee:ff, 1, 2, 3\n"
                    "a3:bb:cc:dd:ee:ff, 1, 2, 3\n"
                    "a4:bb:cc:dd:ee:ff, 1, 2, 3\n"
                )
                bpu.process_csv('test.csv', "client_id", [], "token")
        self.assertEqual("Error: Conflict [409]: child \"profile\" fails because [child \"applications\" fails because [\"applications\" is required]]",
                         exit_context.exception.code)

    @patch("batch_player_upgrade.update_player_profile")
    @patch("batch_player_upgrade.validate_row")
    def test_process_csv_exits_if_update_player_profile_exits_on_409_system_error(self,
                                                                              mock_row_validator,
                                                                              mock_update_player_profile):
        mock_update_player_profile.return_value.status = 500
        mock_update_player_profile.return_value.body = json.dumps({ "statusCode": 500,
                                                                    "error": "Internal Server Error",
                                                                    "message": "An internal server error occurred"})
        mock_row_validator.return_value = [False, True, True, True, True]
        with self.assertRaises(SystemExit) as exit_context:
            with patch.object(builtins, 'open') as mock_file:
                mock_file.return_value = StringIO(
                    "MAC addresses, id1, id2, id3\n"
                    "a1:bb:cc:dd:ee:ff, 1, 2, 3\n"
                    "a2:bb:cc:dd:ee:ff, 1, 2, 3\n"
                    "a3:bb:cc:dd:ee:ff, 1, 2, 3\n"
                    "a4:bb:cc:dd:ee:ff, 1, 2, 3\n"
                )
                bpu.process_csv('test.csv', "client_id", [], "token")
        self.assertEqual("Error: Internal Server Error [500]: An internal server error occurred",
                         exit_context.exception.code)


if __name__ == '__main__':
    unittest.main()
