# Batch Player Upgrade
A simple script to take a list of mac addresses from a csv file and to send a player upgrade request to an API for each one found 
## Installation
copy the script "batch_player_upgrade.py" to your preferred directory

## Configuring the script for use
Before running the script, ensure that the following environment variable is set:
- BPU_API_SERVER=[your_api_server_url]

Alternatively, before distributing the script, you can modify the following line:

- API_SERVER_BASE_URL = os.getenv("BPU_API_SERVER", "http://localhost:8000")

to
- API_SERVER_BASE_URL = os.getenv("BPU_API_SERVER", [your_api_server])


## Running the script
Ensure that you have python version > 3.5 installed on your machine
in a command line shell, change directories to location of the script
copy the csv file to a known path, and run the script with the path to the csv file as the first parameter

```
cd \path\to\script
python batch_player_upgrade {path_to_csv}
```

for more information on usage the script can be called with the -h flag
```
cd \path\to\script
python batch_player_upgrade -h

usage: batch_player_upgrade.py [-h] [-c CLIENT_ID] [-a AUTH_TOKEN]
                               [-m MUSIC_APP] [-d DIAGNOSTIC_APP]
                               [-s SETTINGS_APP]
                               path_to_csv

positional arguments:
  path_to_csv           The path to the csv file containing the MAC address of
                        players to upgrade in the first column

optional arguments:
  -h, --help            show this help message and exit
  -c CLIENT_ID, --client_id CLIENT_ID
                        The id of the client whose players are to be updated
                        [default: dummy_client_id]
  -a AUTH_TOKEN, --auth_token AUTH_TOKEN
                        The authentication token for the API server, if not
                        provided the script will attempt to acquire one
  -m MUSIC_APP, --music_app MUSIC_APP
                        The new version number for the music app
  -d DIAGNOSTIC_APP, --diagnostic_app DIAGNOSTIC_APP
                        The new version number for the diagnostic app
  -s SETTINGS_APP, --settings_app SETTINGS_APP
                        The new version number for the settings app

```
## Running tests
Tests can be run from the root of the source code directory using the following:
```
python -m unittest discover -s tests
```

If you want to run the tests with coverage, the coverage module will need to be installed. This can be done with the following command:
```
pip install -r requirements-test.txt
```

To run the tests with coverage,enter the following command:
```
coverage run -m unittest discover -s tests
```

To see the coverage report, type the following:
```
coverage report -m
```