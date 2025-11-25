from enum import Enum
from typing import Dict, Optional
from django.conf import settings
from django.core.exceptions import PermissionDenied

import requests
from strava.types import RefreshStravaAuthDict, InitialStravaAuthDict


class CONVERSION_NON_MOVING_ACTIVITIES(Enum):
    CF = "Crossfit"
    HIT = "High Intensity Interval Training"
    WT = "Weight Training"
    WO = "Workout"
    Y = "Yoga"
    P = "Pilates"


class CONVERSION_STATIONARY_MOVING_ACTIVITIES(Enum):
    E = "Elliptical"
    RC = "Rock Climbing"
    STS = "Stair Stepper"
    VR = "Virtual Ride"
    VRU = "Virtual Run"
    VRO = "VirtualRow"


class CONVERSION_MOVING_ACTIVITIES(Enum):
    AS = "Alpine Ski"
    BS = "Backcountry Ski"
    C = "Canoeing"
    EBR = "E-Bike Ride"
    G = "Golf"
    HC = "Handcycle"
    H = "Hike"
    IS = "Ice Skate"
    ILS = "Inline Skate"
    K = "Kayaking"
    KS = "Kitesurf"
    NS = "Nordic Ski"
    R = "Ride"
    RS = "Roller Ski"
    ROW = "Rowing"
    RU = "Running"
    S = "Sailing"
    SB = "Skateboard"
    SNB = "Snowboard"
    SS = "Snowshoe"
    SO = "Soccer"
    SUP = "Stand Up Paddling"
    SU = "Surfing"
    SW = "Swim"
    V = "Velomobile"
    W = "Walk"
    WC = "Wheelchair"
    WS = "Windsurf"


class STRAVA_MODEL_CONVERSION(Enum):
    strava_id = "id"
    name = "name"
    elapsed_time = "elapsed_time"
    external_id = "external_id"
    upload_id = "upload_id"

    timezone = "timezone"
    utc_offset = "utc_offset"
    location_city = "location_city"
    location_state = "location_state"
    location_country = "location_country"
    achievement_count = "achievement_count"
    kudos_count = "kudos_count"
    comment_count = "comment_count"
    athlete_count = "athlete_count"
    photo_count = "photo_count"
    device_name = "device_name"
    trainer = "trainer"
    commute = "commute"
    manual = "manual"
    private = "private"
    flagged = "flagged"
    gear_id = "gear_id"
    from_accepted_tag = "from_accepted_tag"
    sport_type = "sport_type"
    distance = "distance"
    average_speed = "average_speed"
    max_speed = "max_speed"
    average_cadence = "average_cadence"
    average_watts = "average_watts"
    weighted_average_watts = "weighted_average_watts"
    kilojoules = "kilojoules"
    device_watts = "device_watts"
    has_heartrate = "has_heartrate"
    average_heartrate = "average_heartrate"
    max_heartrate = "max_heartrate"
    max_watts = "max_watts"
    pr_count = "pr_count"
    total_photo_count = "total_photo_count"
    has_kudoed = "has_kudoed"
    suffer_score = "suffer_score"
    moving_time = "moving_time"
    total_elevation_gain = "total_elevation_gain"


    @classmethod
    def has_key(cls, name):
        return name in cls.__members__

    @classmethod
    def has_value(cls, value):
        return value in set(item.value for item in cls)


class STRAVA_MODEL_DATE_CONVERSION(Enum):
    start_date = "start_date"
    start_date_local = "start_date_local"

    @classmethod
    def has_key(cls, name):
        return name in cls.__members__

    def has_value(cls, value):
        return value in set(item.value for item in cls)

    # start_latitude  = 'start_latitude '
    # start_longitude = 'start_longitude'
    # end_latitude  = 'end_latitude '
    # end_longitude = 'end_longitude'


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


def send_strava_post(
    data, access_token: str, url: str, headers: Optional[Dict[str, str]] = None
):
    BASE_URL = settings.STRAVA_BASE_URL
    URL = f"{BASE_URL}/{url}"
    if headers is None:
        headers = {}
    headers["Authorization"] = f" Bearer {access_token}"
    post_request = requests.post(URL, headers=headers, data=data)
    if post_request.status_code != 200:
        raise PermissionDenied

    post_request_json = post_request.json()

    return post_request_json


def send_strava_get(
    access_token: str, url: str, headers: Optional[Dict[str, str]] = None
):
    BASE_URL = settings.STRAVA_BASE_URL
    URL = f"{BASE_URL}/{url}"
    if headers is None:
        headers = {}
    headers["Authorization"] = f" Bearer {access_token}"
    post_request = requests.get(URL, headers=headers)
    if post_request.status_code != 200:
        raise PermissionDenied
    post_request_json = post_request.json()
    return post_request_json


def api_response_generator(user, url):
    access_token = user.get_access_token()
    data = send_strava_get(access_token, url, headers={"per_page": 30})
    page_counter = 2
    while data:
        for data_section in data:
            yield data_section
        data = send_strava_get(
            access_token, url, headers={"per_page": 30, "page": page_counter}
        )
        page_counter = page_counter + 1
