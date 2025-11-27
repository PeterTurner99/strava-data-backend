from ninja import ModelSchema
from .models import (
    BaseActivity,
    MovingActivity,
    NonMovingActivity,
    StationaryMovingActivity,
    ActivityMap,
)
from ninja.orm import create_schema


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

        exclude = (
            [
                "user",
                "timezone",
                "utc_offset",
                "trainer",
                "commute",
                "manual",
                "flagged",
                "from_accepted_tag",
            ],
        )
