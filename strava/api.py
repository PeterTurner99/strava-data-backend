from ninja import Router
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import get_user_model
from ninja.security import django_auth
from django.conf import settings
from datetime import datetime
from strava.models import (
    ActivityMap,
    BaseActivity,
    MovingActivity,
    NonMovingActivity,
    StationaryMovingActivity,
)
from strava.utils import (
    CONVERSION_MOVING_ACTIVITIES,
    CONVERSION_NON_MOVING_ACTIVITIES,
    CONVERSION_STATIONARY_MOVING_ACTIVITIES,
    STRAVA_MODEL_DATE_CONVERSION,
    api_response_generator,
    STRAVA_MODEL_CONVERSION
)

router = Router()
User = get_user_model()


# obj_data = {
        #     'user': request.user ,
        #     'strava_id':data.get('id') ,
        #     'sport_type': sport_type,
        #     'name': data.get('name'),
        #     'elapsed_time': ,
        #     'external_id': ,
        #     'upload_id': ,
        #     'start_date': ,
        #     'start_date_local': ,
        #     'timezone': ,
        #     'utc_offset': ,
        #     'location_city': ,
        #     'location_state': ,
        #     'location_country': ,
        #     'achievement_count': ,
        #     'kudos_count': ,
        #     'comment_count': ,
        #     'athlete_count': ,
        #     'photo_count': ,
        #     'device_name': ,
        #     'trainer': ,
        #     'commute': ,
        #     'manual': ,
        #     'private': ,
        #     'flagged': ,
        #     'gear_id': ,
        #     'from_accepted_tag': ,
        # }

@ensure_csrf_cookie
@router.get("pull_activities/", auth=django_auth)
def pull_activities(request):
    user = request.user
    NON_MOVING_TYPES = settings.NON_MOVING_TYPES
    STATIONARY_MOVING_TYPES = settings.STATIONARY_MOVING_TYPES
    MOVING_TYPES = settings.MOVING_TYPES

    for data in api_response_generator(user, "athlete/activities"):
        if (BaseActivity.Objects.filter(strava_id=data.get("id"))).exists():
            continue
        sport_type = data.get("sport_type")
        
        obj_data = {}
        for key, value in data.items():
            if value is None:
                continue
            if STRAVA_MODEL_CONVERSION.has_value(key):
                obj_data[STRAVA_MODEL_CONVERSION[key].name] = value
            elif STRAVA_MODEL_DATE_CONVERSION.has_value(key):
                obj_data[STRAVA_MODEL_CONVERSION[key].name] = datetime.fromisoformat(value)
            elif key == 'start_latlng':
                obj_data['start_latitude'] = value[0]
                obj_data['start_longitude'] = value[0]
            elif key == 'end_latlng':
                obj_data['end_latitude'] = value[0]
                obj_data['end_longitude'] = value[0]
        if sport_type in NON_MOVING_TYPES:
            converted_sport_type = CONVERSION_NON_MOVING_ACTIVITIES(sport_type).name
            obj_data["sport_type"] = converted_sport_type
            activity = NonMovingActivity.objects.create(**obj_data)
        elif sport_type in STATIONARY_MOVING_TYPES:
            converted_sport_type = CONVERSION_STATIONARY_MOVING_ACTIVITIES(sport_type).name
            obj_data["sport_type"] = converted_sport_type
            
            
            activity = StationaryMovingActivity.objects.create(**obj_data)
        elif sport_type in MOVING_TYPES:
            converted_sport_type = CONVERSION_MOVING_ACTIVITIES(sport_type).name
            obj_data["sport_type"] = converted_sport_type
            
            
            activity = MovingActivity.objects.create(**obj_data)

            map_data = data.get("map")
            map_obj = ActivityMap.objects.create(
                moving_activity=activity,
                strava_id=data.get("id"),
                polyline=data.get("polyline"),
                summary_polyline=data.get("summary_polyline"),
            )

        else:
            continue
    return 200, {"message": "success"}
