from typing import List
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
from strava.schema import BaseActivitySchema, MovingActivitySchema
from strava.utils import (
    CONVERSION_MOVING_ACTIVITIES,
    CONVERSION_NON_MOVING_ACTIVITIES,
    CONVERSION_STATIONARY_MOVING_ACTIVITIES,
    STRAVA_MODEL_DATE_CONVERSION,
    api_response_generator,
    STRAVA_MODEL_CONVERSION,
)
from ninja.errors import HttpError
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
        if (BaseActivity.objects.filter(strava_id=data.get("id"))).exists():
            continue
        sport_type = data.get("sport_type")

        obj_data = {"user": request.user}
        if sport_type in NON_MOVING_TYPES:
            model = NonMovingActivity
            enum = CONVERSION_NON_MOVING_ACTIVITIES
        elif sport_type in STATIONARY_MOVING_TYPES:
            model = StationaryMovingActivity
            enum = CONVERSION_STATIONARY_MOVING_ACTIVITIES
        elif sport_type in MOVING_TYPES:
            model = MovingActivity
            enum = CONVERSION_MOVING_ACTIVITIES

        for key, value in data.items():
            if value is None:
                continue
            fields = [field.name for field in model._meta.get_fields()]
            if STRAVA_MODEL_CONVERSION.has_value(key):
                field_name = STRAVA_MODEL_CONVERSION(key).name
                
                if field_name not in fields:
                    continue
                obj_data[field_name] = value
            elif STRAVA_MODEL_DATE_CONVERSION.has_value(key):
                obj_data[STRAVA_MODEL_DATE_CONVERSION(key).name] = (
                    datetime.fromisoformat(value)
                )
            elif key == "start_latlng":
                field_name = 'end_longitude'
                if value == []:
                    continue
                if field_name not in fields:
                    continue
                obj_data["start_latitude"] = value[0]
                obj_data["start_longitude"] = value[0]
            elif key == "end_latlng":
                if value == []:
                    continue
                if field_name not in fields:
                    continue
                obj_data["end_latitude"] = value[0]
                obj_data["end_longitude"] = value[0]
        converted_sport_type = enum(sport_type).name
        obj_data["sport_type"] = converted_sport_type
        activity = model.objects.create(**obj_data)

        if sport_type in MOVING_TYPES:
            map_data = data.get("map")
            map_obj = ActivityMap.objects.create(
                moving_activity=activity,
                strava_id=map_data.get("id"),
                polyline=map_data.get("polyline", ""),
                summary_polyline=map_data.get("summary_polyline", ""),
            )

        else:
            continue
    return 200, {"message": "success"}



@ensure_csrf_cookie
@router.get('base_activities/', auth=django_auth, response=List[BaseActivitySchema])
def get_base_activities(request, limit: int = 30, offset: int = 0):
    base_activities = BaseActivity.objects.filter(user=request.user).order_by('-start_date')[(offset*limit): (offset*limit) + limit]
    return base_activities

@ensure_csrf_cookie
@router.get('base_activity/{id}/', auth=django_auth, response=BaseActivitySchema)
def get_base_activity(request, id: int):
    base_activity = BaseActivity.objects.filter(id=id).order_by('-start_date')
    if not base_activity.exists():
       raise HttpError (404, 'Item not found')
    base_activity = base_activity.first()
    if base_activity.user != request.user:
        raise HttpError(403, 'Not correct user')
    return base_activity


@ensure_csrf_cookie
@router.get('moving_activities/', auth=django_auth, response=List[MovingActivitySchema])
def get_moving_activities(request, limit: int = 30, offset: int = 0):
    moving_activities = MovingActivity.objects.filter(user=request.user).order_by('-start_date')[(offset*limit): (offset*limit) + limit]
    return moving_activities

@ensure_csrf_cookie
@router.get('moving_activity/{id}/', auth=django_auth, response=MovingActivitySchema)
def get_moving_activity(request, id: int):
    moving_activity = MovingActivity.objects.filter(id=id).order_by('-start_date')
    if not moving_activity.exists():
       raise HttpError (404, 'Item not found')
    moving_activity = moving_activity.first()
    if moving_activity.user != request.user:
        raise HttpError(403, 'Not correct user')
    return moving_activity

