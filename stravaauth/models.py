from typing import Self
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.core.exceptions import PermissionDenied
from strava.utils import send_strava_post_auth
# Create your models here.


class StravaAthlete(AbstractUser):
    MEASUREMENT_CHOICES = [
        ("F", "Feet"),
        ("M", "Meters"),
    ]
    athelete_id = models.IntegerField()
    measurement_preference = models.CharField(choices=MEASUREMENT_CHOICES, max_length=5)
    ftp = models.IntegerField(null= True, blank=True)
    weight = models.FloatField()
    access_token = models.CharField(max_length=120)
    refresh_token = models.CharField(max_length=120)
    expires_at_int = models.IntegerField()
    activities_last_checked = models.DateTimeField(blank=True, null=True)
    @property
    def expires_at(self: Self) -> datetime:
        return datetime.fromtimestamp(self.expires_at_int)

    def update_refresh_token(self: Self) -> None:
        data = {"refresh_token": self.refresh_token, "grant_type": "refresh_token"}
        if not send_strava_post_auth(data, self):
            raise PermissionDenied()
    
    def get_access_token(self: Self) -> str:
        if self.expires_at < datetime.now():
            self.update_refresh_token()

        return self.access_token
