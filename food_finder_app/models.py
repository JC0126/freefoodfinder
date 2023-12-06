from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from address.models import AddressField
import datetime

# Create your models here.
from django.contrib.auth.models import Group


class CustomGroup(Group):
    description = models.TextField(blank=True)


class Event(models.Model):
    event_title = models.CharField(max_length=200)
    event_description = models.CharField(
        max_length=560
    )  # double the length of a maximum length tweet
    available_to = models.CharField(max_length=9)  # comma seperated integer list where
    # address = AddressField(on_delete=models.CASCADE)
    # 1,2,3 means available to first second and third years
    # 0 means available to everyone
    # https://docs.djangoproject.com/en/dev/ref/validators/#django.core.validators.validate_comma_separated_integer_list
    event_start_date = models.DateTimeField("event start time", default=timezone.now)
    # event_duration = models.DurationField("event duration", default=datetime.timedelta())
    event_end_date = models.DateTimeField("event end time", default=timezone.now)
    event_lattitude = models.DecimalField(
        "lattitude", max_digits=20, decimal_places=8
    )
    event_longitude = models.DecimalField("longitude", max_digits=20, decimal_places=8)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.event_description

    def get_location(self):
        return self.event_longitude, self.event_lattitude

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.event_date <= now

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
