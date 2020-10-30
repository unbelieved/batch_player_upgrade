#!/bin/python3
# This a simple python script for updating players in bulk using a .csv file containing MAC addresses.
import argparse
import csv
import json
import os
import re
import sys
from urllib import request

API_SERVER_BASE_URL = os.getenv("BPU_API_SERVER", "http://localhost:8000")


def batch_player_upgrade():
    client_id = get_client_id()

    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_csv",
                        help="The path to the csv file containing the MAC address of players to upgrade in the first "
                             "column")
    parser.add_argument("-c", "--client_id",
                        default=client_id,
                        help="The id of the client whose players are to be updated [default: {}]".format(client_id))
    parser.add_argument("-a",
                        "--auth_token",
                        help="The authentication token for the API server, if not provided the script will attempt to "
                             "acquire one")
    parser.add_argument("-m", "--music_app", default="v1.4.10", help="The new version number for the music app")
    parser.add_argument("-d", "--diagnostic_app", default="v1.2.6", help="The new version number for the diagnostic app")
    parser.add_argument("-s", "--settings_app", default="v1.1.5", help="The new version number for the settings app")

    args = parser.parse_args()
    auth_token = args.auth_token
    client_id = args.client_id

    if os.path.isfile(args.path_to_csv):
        if auth_token is None:
            auth_token = get_authentication_token()

        applications = [{"applicationId": "music_app", "version": args.music_app},
                        {"applicationId": "diagnostic_app", "version": args.diagnostic_app},
                        {"applicationId": "settings_app", "version": args.settings_app}]

        process_csv(args.path_to_csv, client_id, applications, auth_token)

    else:
        print("File not found: '{}'".format(args.path_to_csv), file=sys.stderr)
        sys.exit(1)


def get_authentication_token():
    return "dummy_authentication_token"


def get_client_id():
    return "dummy_client_id"


def process_csv(csv_file_path, client_id, applications, token):
    with open(csv_file_path) as csv_file:
        csv_data = csv.reader(csv_file)
        for row in csv_data:
            if validate_row(row):
                line_update_response = update_player_profile(client_id, row[0], applications, token)
                response_status = getattr(line_update_response, "status", "")
                if response_status > 399:
                    response_data = json.loads(line_update_response.body)
                    sys.exit("Error: {error} [{statusCode}]: {message}".format(**response_data))

            elif csv_data.line_num != 1:
                print("Line {}: Warning: Column 1 does not contain a valid Mac Address".format(csv_data.line_num))


def validate_row(row):
    if len(row) == 0:
        return False
    return hasattr(re.match("^([0-9|A-F]{2}:){5}[0-9|A-F]{2}$", row[0], re.I), "groups")


def update_player_profile(client_id, mac_address, applications, token):
    request_url = "{}/profiles/clientId:{}".format(API_SERVER_BASE_URL, mac_address)
    request_data = bytes(json.dumps({"profile": {"applications": applications}}), encoding='utf8')
    request_headers = {"Content-Type": "application/json", "x-client-id": client_id, "x-authentication-token": token}

    update_request = request.Request(request_url, data=request_data, method="PUT", headers=request_headers)
    response = request.urlopen(update_request)

    return response


if __name__ == '__main__':
    batch_player_upgrade()
