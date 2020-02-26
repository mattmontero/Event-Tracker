import base64
import os

import requests

from requests.auth import HTTPBasicAuth

ACCESS_TOKEN_URL = "https://api.stubhub.com/sellers/oauth/accesstoken?grant_type=client_credentials"
EVENTS_URL = "https://api.stubhub.com/sellers/search/events/v3"

ACCESS_TOKEN = os.getenv("STUBHUB_ACCESS_TOKEN", None)


def get_events(keyword: str, params: dict):
    params.update({
        "name": keyword,
        "parking": "false"
    })

    headers = {
        'Authorization': f"Bearer {ACCESS_TOKEN}"
    }

    resp = requests.get(url=EVENTS_URL, headers=headers, params=params)
    if resp.ok:
        return resp.json()
    return None


def get_access_token(app_key, app_secret, stubhub_username, stubhub_password):
    encoded = base64.b64encode(bytes(f"{app_key}:{app_secret}", 'utf-8')).decode('utf-8')
    basic_auth = f"Basic {encoded}"

    headers = {
        "Authorization": basic_auth,
        "Content-Type": "application/json",
    }
    data = {
        "username": stubhub_username,
        "password": stubhub_password
    }

    resp = requests.post(url=ACCESS_TOKEN_URL, data=data, headers=headers)
    if not resp.ok:
        return resp
    if 'access_token' in resp.json:
        return resp.json['access_token']
