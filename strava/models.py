from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.IntegerField()
    name = models.CharField(blank=True, null=True)


class MovingActivity(BaseActivity):
    moving_time = models.IntegerField()
    distance = models.FloatField()