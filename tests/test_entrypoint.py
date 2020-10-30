import sys
import unittest
from io import StringIO
from unittest.mock import patch

import batch_player_upgrade as bpu


class TestEntryPoint(unittest.TestCase):

    @patch('sys.stderr', new_callable=StringIO)
    def test_script_raises_error_called_without_parameters(self, mock_output):
        test_args = ["batch_player_upgrade"]
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(SystemExit) as exit_context:
                bpu.batch_player_upgrade()
            self.assertGreater(exit_context.exception.code, 0)
            self.assertIn("batch_player_upgrade: error: the following arguments are required: path_to_csv",
                          mock_output.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    def test_script_returns_usage_when_called_without_parameters(self, mock_output):
        test_args = ["batch_player_upgrade"]
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(SystemExit) as exit_context:
                bpu.batch_player_upgrade()
            self.assertIn("usage: batch_player_upgrade", mock_output.getvalue())

    @patch("os.path.isfile")
    @patch('sys.stderr', new_callable=StringIO)
    def test_exits_with_message_when_file_not_found(self, mock_output, mock_isfile):
        test_args = ["batch_player_upgrade", "non_existent_file"]
        mock_isfile.return_value = False
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(SystemExit) as exit_context:
                bpu.batch_player_upgrade()
            self.assertGreater(exit_context.exception.code, 0)
            self.assertIn("File not found: 'non_existent_file'", mock_output.getvalue())

    @patch("batch_player_upgrade.get_client_id")
    @patch('sys.stdout', new_callable=StringIO)
    def test_default_client_id_is_populated_using_the_get_client_id_function(self, mock_output, mock_get_client_id):
        mock_get_client_id.return_value = "test_client_id"
        test_args = ["batch_player_upgrade", "-h"]
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(SystemExit) as exit_context:
                bpu.batch_player_upgrade()

        assert mock_get_client_id.called
        self.assertIn("[default: test_client_id]", mock_output.getvalue())

    @patch("batch_player_upgrade.get_authentication_token")
    @patch("batch_player_upgrade.process_csv")
    @patch("os.path.isfile")
    def test_get_authentication_token_called_if_file_is_valid_and_token_not_provided(self,
                                                                                     mock_is_file,
                                                                                     mock_process_csv,
                                                                                     mock_get_token):
        mock_get_token.return_value = "test_token"
        mock_is_file.return_value = True
        test_args = ["batch_player_upgrade", "csv_file"]
        with patch.object(sys, 'argv', test_args):
            bpu.batch_player_upgrade()
        assert mock_get_token.called
        assert mock_process_csv.called

    @patch("batch_player_upgrade.get_authentication_token")
    @patch("batch_player_upgrade.process_csv")
    @patch("os.path.isfile")
    def test_get_authentication_token_not_called_if_file_is_valid_and_token_provided(self,
                                                                                     mock_is_file,
                                                                                     mock_process_csv,
                                                                                     mock_get_token):
        mock_get_token.return_value = "test_token"
        mock_is_file.return_value = True
        test_args = ["batch_player_upgrade", "csv_file", "-a", "new_token"]
        with patch.object(sys, 'argv', test_args):
            bpu.batch_player_upgrade()
        assert not mock_get_token.called
        assert mock_process_csv.called

    @patch("batch_player_upgrade.get_authentication_token")
    @patch("batch_player_upgrade.get_client_id")
    @patch("batch_player_upgrade.process_csv")
    @patch("os.path.isfile")
    def test_process_csv_called_with_defaults_if_only_file_is_provided(self,
                                                                       mock_is_file,
                                                                       mock_process_csv,
                                                                       mock_get_client_id,
                                                                       mock_get_token):
        mock_get_token.return_value = "test_token"
        mock_get_client_id.return_value = "test_client_id"
        mock_is_file.return_value = True

        default_applications = [{"applicationId": "music_app", "version": "v1.4.10"},
                                {"applicationId": "diagnostic_app", "version": "v1.2.6"},
                                {"applicationId": "settings_app", "version": "v1.1.5"}]

        test_args = ["batch_player_upgrade", "csv_file"]
        with patch.object(sys, 'argv', test_args):
            bpu.batch_player_upgrade()

        mock_process_csv.assert_called_with("csv_file", "test_client_id", default_applications, "test_token")

    @patch("batch_player_upgrade.get_authentication_token")
    @patch("batch_player_upgrade.get_client_id")
    @patch("batch_player_upgrade.process_csv")
    @patch("os.path.isfile")
    def test_process_csv_called_with_overriden_defaults_if_provided(self,
                                                                    mock_is_file,
                                                                    mock_process_csv,
                                                                    mock_get_client_id,
                                                                    mock_get_token):
        mock_get_token.return_value = "test_token"
        mock_get_client_id.return_value = "test_client_id"
        mock_is_file.return_value = True
        new_applications = [{"applicationId": "music_app", "version": "v1.4.11"},
                                {"applicationId": "diagnostic_app", "version": "v1.2.7"},
                                {"applicationId": "settings_app", "version": "v1.1.6"}]

        test_args = ["batch_player_upgrade",
                     "csv_file",
                     "-a", "new_token",
                     "-c", "new_client_id",
                     "-m", "v1.4.11",
                     "-d", "v1.2.7",
                     "-s", "v1.1.6"]
        with patch.object(sys, 'argv', test_args):
            bpu.batch_player_upgrade()

        mock_process_csv.assert_called_with("csv_file", "new_client_id", new_applications, "new_token")


if __name__ == '__main__':
    unittest.main()
