import json
import unittest
from unittest.mock import patch

import batch_player_upgrade as bpu


class TestUpdatePlayerProfile(unittest.TestCase):

    @patch("urllib.request.urlopen")
    @patch("urllib.request.Request")
    @patch("batch_player_upgrade.API_SERVER_BASE_URL", "http://example.com")
    def test_update_player_profile_calls_Request(self, mock_request, mock_urlopen):
        bpu.update_player_profile("test_client_id", "test_macaddress", [], "test_token")
        assert mock_request.is_called_with("http://example.com/profiles/clientID:test_macaddress",
                                           data=bytes(json.dumps({"profile": {"applications": []}}), encoding='utf8'),
                                           method="PUT",
                                           headers={"Content-Type": "application/json",
                                                    "x-client-id": "test_client_id",
                                                    "x-authentication-token": "test_token"})

    @patch("urllib.request.urlopen")
    @patch("batch_player_upgrade.API_SERVER_BASE_URL", "http://example.com")
    def test_update_player_profile_creates_request_with_correct_address(self, mock_urlopen):
        bpu.update_player_profile("test_client_id", "test_macaddress", [], "test_token")
        assert mock_urlopen.call_args[0][0].full_url == "http://example.com/profiles/clientId:test_macaddress"


    @patch("urllib.request.urlopen")
    @patch("batch_player_upgrade.API_SERVER_BASE_URL", "http://example.com")
    def test_update_player_profile_creates_request_with_correct_body(self, mock_urlopen):
        applications = [{"applicationId": "music_app", "version": "v1.4.10"},
                        {"applicationId": "diagnostic_app", "version": "v1.2.6"},
                        {"applicationId": "settings_app", "version": "v1.1.5"}]

        expected_body = {
              "profile": {
                "applications": [
                  {
                    "applicationId": "music_app",
                    "version": "v1.4.10"
                  },
                  {
                    "applicationId": "diagnostic_app",
                    "version": "v1.2.6"
                  },
                  {
                    "applicationId": "settings_app",
                    "version": "v1.1.5"
                  }
                ]
              }
            }

        bpu.update_player_profile("test_client_id", "test_macaddress", applications, "test_token")
        assert mock_urlopen.call_args[0][0].data == bytes(json.dumps(expected_body), encoding='utf8')

    @patch("urllib.request.urlopen")
    def test_update_player_profile_creates_request_with_correct_headers(self, mock_urlopen):
        bpu.update_player_profile("test_client_id", "test_macaddress", [], "test_token")

        assert mock_urlopen.call_args[0][0].get_header("Content-type") == "application/json"
        assert mock_urlopen.call_args[0][0].get_header("X-client-id") == "test_client_id"
        assert mock_urlopen.call_args[0][0].get_header("X-authentication-token") == "test_token"

    @patch("urllib.request.urlopen")
    def test_update_player_profile_returns_response_from_request(self, mock_request):
        assert bpu.update_player_profile("", "", [], "") == mock_request.return_value


if __name__ == '__main__':
    unittest.main()
