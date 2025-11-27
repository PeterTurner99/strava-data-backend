from django.contrib import admin
from .models import BaseActivity, MovingActivity, ActivityMap
# Register your models here.
admin.site.register(BaseActivity)
admin.site.register(MovingActivity)
admin.site.register(ActivityMap)