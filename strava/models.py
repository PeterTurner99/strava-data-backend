from django.db import models
from typing import Self
# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()


NON_MOVING_ACTIVITIES = [
    (Crossfit := "CF", "Crossfit"),
    (HighIntensityIntervalTraining := "HIT", "High Intensity Interval Training"),
    (WeightTraining := "WT", "Weight Training"),
    (Workout := "WO", "Workout"),
    (Yoga := "Y", "Yoga"),
    (Pilates := "P", "Pilates"),
]
STATIONARY_MOVING_ACTIVITIES = [
    (Elliptical := "E", "Elliptical"),
    (RockClimbing := "RC", "Rock Climbing"),
    (StairStepper := "STS", "Stair Stepper"),
    (VirtualRide := "VR", "Virtual Ride"),
    (VirtualRun := "VRU", "Virtual Run"),
    (VirtualRow := "VRO", "VirtualRow"),
]
MOVING_ACTIVITIES = [
    (AlpineSki := "AS", "Alpine Ski"),
    (BackcountrySKI := "BS", "Backcountry Ski"),
    (Canoeing := "C", "Canoeing"),
    (EBikeRide := "EBR", "E-Bike Ride"),
    (Golf := "G", "Golf"),
    (GravelRide := 'GR', 'Gravel Ride'),
    (Handcycle := "HC", "Handcycle"),
    (Hike := "H", "Hike"),
    (IceSkate := "IS", "Ice Skate"),
    (InlineSkate := "ILS", "Inline Skate"),
    (Kayaking := "K", "Kayaking"),
    (Kitesurf := "KS", "Kitesurf"),
    (NordicSki := "NS", "Nordic Ski"),
    (Ride := "R", "Ride"),
    (RollerSki := "RS", "Roller Ski"),
    (Rowing := "ROW", "Rowing"),
    (Run := "RU", "Running"),
    (Sail := "S", "Sailing"),
    (Skateboard := "SB", "Skateboard"),
    (Snowboard := "SNB", "Snowboard"),
    (Snowshoe := "SS", "Snowshoe"),
    (Soccer := "SO", "Soccer"),
    (StandUpPaddling := "SUP", "Stand Up Paddling"),
    (Surfing := "SU", "Surfing"),
    (Swim := "SW", "Swim"),
    (Velomobile := "V", "Velomobile"),
    (Walk := "W", "Walk"),
    (Wheelchar := "WC", "Wheelchair"),
    (Windsurf := "WS", "Windsurf"),
]
"""
Activity Type has less options than Sports Type
Type is depracated
So both are not used


"""


class BaseActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    strava_id = models.IntegerField()
    name = models.CharField(blank=True, null=True)
    elapsed_time = models.IntegerField()
    external_id = models.CharField(max_length=100, null=True, blank=True)
    upload_id = models.IntegerField(null=True, blank=True)
    start_date = models.DateTimeField()
    start_date_local = models.DateTimeField()
    timezone = models.CharField(max_length=100)
    utc_offset = models.IntegerField()
    location_city = models.CharField(max_length=125, null=True, blank=True)
    location_state = models.CharField(max_length=125, null=True, blank=True)
    location_country = models.CharField(max_length=125, null=True, blank=True)
    achievement_count = models.IntegerField()
    kudos_count = models.IntegerField()
    comment_count = models.IntegerField()
    athlete_count = models.IntegerField()
    photo_count = models.IntegerField()
    device_name = models.CharField(max_length=125, null=True, blank=True)
    trainer = models.BooleanField(default=False)
    commute = models.BooleanField(default=False)
    manual = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)
    gear_id = models.CharField(max_length=125, null=True, blank=True)
    from_accepted_tag = models.BooleanField(default=False)
    @property
    def start_date_str(self: Self) -> str:
        return f"{self.start_date.timestamp()}"

class NonMovingActivity(BaseActivity):
    sport_type = models.CharField(choices=NON_MOVING_ACTIVITIES, max_length=10)
    total_photo_count = models.IntegerField(default=0)
    has_kudoed = models.BooleanField(default=False)

class StationaryMovingActivity(BaseActivity):
    distance = models.FloatField()
    sport_type = models.CharField(
        choices=NON_MOVING_ACTIVITIES + STATIONARY_MOVING_ACTIVITIES, max_length=10
    )
    average_speed = models.FloatField()
    max_speed = models.FloatField()
    average_cadence = models.FloatField(null=True, blank=True)
    average_watts = models.FloatField(null=True, blank=True)
    weighted_average_watts = models.IntegerField(null=True, blank=True)
    kilojoules = models.FloatField(null=True, blank=True)
    device_watts = models.BooleanField(default=False)
    has_heartrate = models.BooleanField(default=False)
    average_heartrate = models.FloatField(null=True, blank=True)
    max_heartrate = models.FloatField(null=True, blank=True)
    max_watts = models.IntegerField(null=True, blank=True)
    pr_count = models.IntegerField(default=0)
    total_photo_count = models.IntegerField(default=0)
    has_kudoed = models.BooleanField(default=False)
    suffer_score = models.FloatField(null=True, blank=True)


class MovingActivity(BaseActivity):
    moving_time = models.IntegerField()
    sport_type = models.CharField(
        choices=NON_MOVING_ACTIVITIES
        + STATIONARY_MOVING_ACTIVITIES
        + MOVING_ACTIVITIES,
        max_length=10,
    )
    total_elevation_gain = models.FloatField()
    start_latitude  = models.FloatField(null=True, blank=True)
    start_longitude = models.FloatField(null=True, blank=True)
    end_latitude  = models.FloatField(null=True, blank=True)
    end_longitude = models.FloatField(null=True, blank=True)
    distance = models.FloatField()
    average_speed = models.FloatField()
    max_speed = models.FloatField()
    average_cadence = models.FloatField(null=True, blank=True)
    average_watts = models.FloatField(null=True, blank=True)
    weighted_average_watts = models.IntegerField(null=True, blank=True)
    kilojoules = models.FloatField(null=True, blank=True)
    device_watts = models.BooleanField(default=False)
    has_heartrate = models.BooleanField(default=False)
    average_heartrate = models.FloatField(null=True, blank=True)
    max_heartrate = models.FloatField(null=True, blank=True)
    max_watts = models.IntegerField(null=True, blank=True)
    pr_count = models.IntegerField(default=0)
    total_photo_count = models.IntegerField(default=0)
    has_kudoed = models.BooleanField(default=False)
    suffer_score = models.FloatField(null=True, blank=True)


class ActivityMap(models.Model):
    moving_activity = models.OneToOneField(MovingActivity, on_delete=models.CASCADE)
    strava_id = models.CharField(max_length=125)
    polyline = models.TextField()
    summary_polyline = models.TextField()
