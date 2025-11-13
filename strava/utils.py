from django.conf import settings
from django.core.exceptions import PermissionDenied

import requests
from strava.types import RefreshStravaAuthDict, InitialStravaAuthDict


def send_strava_post_auth(data: RefreshStravaAuthDict, athelete):
    BASE_URL = settings.STRAVA_BASE_URL
    URL = f"{BASE_URL}oauth/token"
    data["client_id"] = settings.CLIENT_ID
    data["client_secret"] = settings.CLIENT_SECRET
    post_request = requests.post(URL, data=data)
    if post_request.status_code != 200:
        return False
    post_request_json = post_request.json()
    athelete.access_token = post_request_json.get("access_token")
    athelete.refresh_token = post_request_json.get("refresh_token")
    athelete.expires_at_int = post_request_json.get("expires_at")
    athelete.save()
    return True


def send_initial_strava_post_auth(data: InitialStravaAuthDict):
    BASE_URL = settings.STRAVA_BASE_URL
    URL = f"{BASE_URL}oauth/token"
    data["client_id"] = settings.CLIENT_ID
    data["client_secret"] = settings.CLIENT_SECRET
    post_request = requests.post(URL, data=data)
    if post_request.status_code != 200:
        return False
    post_request_json = post_request.json()
    return post_request_json


def send_strava_post(data, access_token: str, url: str):
    BASE_URL = settings.STRAVA_BASE_URL
    URL = f"{BASE_URL}/{url}"

    post_request = requests.post(
        URL, headers={"Authorization": f" Bearer {access_token}"}, data=data
    )
    if post_request.status_code != 200:
        raise PermissionDenied

    post_request_json = post_request.json()

    return post_request_json


def send_strava_get(data, access_token: str, url: str):
    BASE_URL = settings.STRAVA_BASE_URL
    URL = f"{BASE_URL}/{url}"

    post_request = requests.get(
        URL, headers={"Authorization": f" Bearer {access_token}"}
    )
    if post_request.status_code != 200:
        raise PermissionDenied
    post_request_json = post_request.json()
    return post_request_json
