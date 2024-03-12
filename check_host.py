import requests

import configparser

config_parser = configparser.ConfigParser()

config_parser.read_string('[default]\n' + open('config.properties').read())

CDMS_properties = {}

for option in config_parser.options('default'):
    CDMS_properties[option] = config_parser.get('default', option)

url = CDMS_properties['main_app']+"dataupload/getUploadStatusConsumer"

params = {"uploadId":37}

headers = {'X-AUTH-TOKEN': CDMS_properties['x-auth-token']}

try:
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        print("Request successful!")
        content = response.text 
        print(content)
    else:
        print(f"Request failed with status code: {response.status_code}")
except Exception as e:
    print(f"An error occurred: {e}")