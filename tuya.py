import logging
from env import ENDPOINT, ACCESS_ID, ACCESS_KEY, USERNAME, PASSWORD
# from example.env import DEVICE_ID
from tuya_iot.openlogging import TUYA_LOGGER
from tuya_iot import (
    TuyaOpenAPI,
    AuthType,
    TuyaOpenMQ,
    TuyaDeviceManager,
    TuyaHomeManager,
    TuyaDeviceListener,
    TuyaDevice,
    TuyaTokenInfo,
    TUYA_LOGGER
)
import requests, json
from typing import Any


class Tuya:
    access_token = ''
    refresh_token = ''
    expire_time = ''
    def __init__(self):
        print('start tuya')
        

    def get_token(self):
        api = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)

        sign, t = api._calculate_sign('GET', '/v1.0/token?grant_type=1', None, None, None)

        url = f"{ENDPOINT}/v1.0/token?grant_type=1"

        payload = {}
        headers = {
            'client_id': ACCESS_ID,
            'sign': sign,
            'sign_method': 'HMAC-SHA256',
            #   "access_token": access_token,
            't': str(t)

        }

        response = requests.request("GET", url, headers=headers, data=payload)
        j = json.loads(response.text)
        self.access_token = j['result']['access_token']
        self.refresh_token = j['result']['refresh_token']
        self.expire_time = j['result']['expire_time']
        print(response.text)

    def refresh_token_function(self):
        api = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)

        sign, t = api._calculate_sign('GET', f'/v1.0/token/{self.refresh_token}', None, None, None)

        url = f"{ENDPOINT}/v1.0/token/{self.refresh_token}"

        payload = {}
        headers = {
            'client_id': ACCESS_ID,
            'sign': sign,
            'sign_method': 'HMAC-SHA256',
            #   "access_token": access_token,
            't': str(t)

        }

        response = requests.request("GET", url, headers=headers, data=payload)
        j = json.loads(response.text)
        self.access_token = j['result']['access_token']
        self.refresh_token = j['result']['refresh_token']
        self.expire_time = j['result']['expire_time']
        print(response.text)

    def get_device_info(self, deviceID: str):
        self.refresh_token_function()
        api = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)

        sign, t = api._calculate_sign('GET', f'/v1.0/devices/{deviceID}',self.access_token, None, None)

        url = f"{ENDPOINT}/v1.0/devices/{deviceID}"

        payload = {}
        headers = {
            'client_id': ACCESS_ID,
            'sign': sign,
            'sign_method': 'HMAC-SHA256',
            "access_token": self.access_token,
            't': str(t)

        }

        response = requests.request("GET", url, headers=headers, data=payload)
        
        print(response.text)

        return json.loads(response.text)

    def sent_commands(self, deviceID: str, command: dict[str, Any]):
        self.refresh_token_function()
        api = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)

        sign, t = api._calculate_sign('POST', f'/v1.0/devices/{deviceID}/commands',self.access_token, None, command)

        url = f"{ENDPOINT}/v1.0/devices/{deviceID}/commands"
        print(command)
        headers = {
            'client_id': ACCESS_ID,
            'sign': sign,
            'sign_method': 'HMAC-SHA256',
            "access_token": self.access_token,
            't': str(t)

        }

        response = requests.request("POST", url, headers=headers, json=command)
        
        print(response.text)

        return json.loads(response.text)
