from django.contrib.auth.models import User
from django.db import models


class CalendarUser(models.Model):
    user = models.OneToOneField(User)
    timezone = models.CharField(max_length=50)

