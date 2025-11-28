from typing import Optional
from ninja import ModelSchema, FilterSchema
from .models import (
    BaseActivity,
    MovingActivity,
    NonMovingActivity,
    StationaryMovingActivity,
    ActivityMap,
)
from datetime import datetime
from django.db.models import Q

class NoneBaseActivityFilterSchema(FilterSchema):
    before: Optional[str] = None
    after: Optional[str] = None
    def filter_before(self, value:str) -> Q:
        if not value:
            return Q()
        date_time = datetime.fromisoformat(value)
        return Q(start_date__lte = date_time)

    def filter_after(self, value:str) -> Q:
        if not value:
            return Q()
        date_time = datetime.fromisoformat(value)
        return Q(start_date__gte = date_time) 
    
class NoneBaseActivityFilterSchema(NoneBaseActivityFilterSchema):
    sport_type: Optional[str] = None
    

class BaseActivitySchema(ModelSchema):
    class Meta:
        model = BaseActivity
        exclude = [
            "user",
            "timezone",
            "utc_offset",
            "trainer",
            "commute",
            "manual",
            "flagged",
            "from_accepted_tag",
        ]


class ActivityMapSchema(ModelSchema):
    class Meta:
        model = ActivityMap
        exclude = ["moving_activity"]


class MovingActivitySchema(ModelSchema):
    activitymap: ActivityMapSchema = None

    class Meta:
        model = MovingActivity
        exclude = [
            "user",
            "timezone",
            "utc_offset",
            "trainer",
            "commute",
            "manual",
            "flagged",
            "from_accepted_tag",
        ]


class MovingActivitySchemaNoMap(ModelSchema):
    class Meta:
        model = MovingActivity
        exclude = [
            "user",
            "timezone",
            "utc_offset",
            "trainer",
            "commute",
            "manual",
            "flagged",
            "from_accepted_tag",
        ]


class NonMovingActivitySchema(ModelSchema):
    class Meta:
        model = NonMovingActivity
        exclude = [
            "user",
            "timezone",
            "utc_offset",
            "trainer",
            "commute",
            "manual",
            "flagged",
            "from_accepted_tag",
        ]


class StationaryMovingActivitySchema(ModelSchema):
    class Meta:
        model = StationaryMovingActivity

        exclude = [
            "user",
            "timezone",
            "utc_offset",
            "trainer",
            "commute",
            "manual",
            "flagged",
            "from_accepted_tag",
        ]
