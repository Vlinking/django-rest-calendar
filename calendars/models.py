from django.db import models
from django.contrib.auth.models import User


class Calendar(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    # will be stored in RGB
    #or better, a custom field can be done
    color = models.CharField(max_length=6)

    def __unicode__(self):
        return self.name



class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    timezone = models.CharField(max_length=50)
    type = models.CharField(max_length=10)
    start = models.TimeField()
    end = models.TimeField()


