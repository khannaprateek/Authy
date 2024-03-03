import os

import urllib.request
import urllib.parse
import requests

APIKEY = os.environ.get('2FACTOR_APIKEY')
APP_SMS_CODE = os.environ.get('APP_SMS_CODE')
BASEURL = 'https://2factor.in/API/V1'

def create_otp(phone_code, phone):
    url = f"{BASEURL}/{APIKEY}/SMS/{phone_code}{phone}/?var1={urllib.parse.quote('<#>')}&var2={urllib.parse.quote(APP_SMS_CODE)}"
    response = requests.request("GET", url)
    if response.json()['Status'] != 'Error':
        print(response.json()['Details'])
        return True, response.json()['Details']
    else:
        print('Error in Sending OTP RESPONSE', response.json()['Details'])
        return False, response.json()['Details']


def verify_otp(session_id, otp):
    url = f"{BASEURL}/{APIKEY}/SMS/VERIFY/{session_id}/{otp}"

    response = requests.request("GET", url)
    if response.json()['Status'] != 'Error':
        print(response.json()['Details'])
        return True
    else:
        print('Error in verifing', response.json()['Details'])
        return False