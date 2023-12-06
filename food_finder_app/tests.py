import datetime
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from .models import Event


def create_event(
        days_start,days_end, event_title = "test", event_description = "there is food", available_to=0, event_longitude=0,
        event_lattitude=0, approved=False):

    event_end_date = timezone.now() + datetime.timedelta(days=days_end)
    event_start_date = timezone.now() + datetime.timedelta(days=days_start)
    return Event.objects.create(
        event_title = event_title,
        event_description=event_description,
        available_to=available_to,
        event_start_date=event_start_date,
        event_end_date=event_end_date,
        event_longitude=event_longitude,
        event_lattitude=event_lattitude,
        approved = approved
    )


class EventModelTests(TestCase):
    # test a past event
    def test_past_events(self):
        event = create_event(-10,-30)
        response = self.client.get("/events/")
        self.assertQuerysetEqual(
            response.context["cur_events"],
            [],
        )
        self.assertQuerysetEqual(
            response.context["future_events"],
            [],
        )

    def test_past_events_approved(self):
        event = create_event(-10,-30, approved=True)
        response = self.client.get("/events/")
        self.assertQuerysetEqual(
            response.context["cur_events"],
            [],
        )
        self.assertQuerysetEqual(
            response.context["future_events"],
            [],
        )

    def test_future_events(self):
        event = create_event(10,30)
        response = self.client.get("/events/")
        self.assertQuerysetEqual(
            response.context["cur_events"],
            [],
        )
        self.assertQuerysetEqual(
            response.context["future_events"],
            [],
        )

    def test_future_events_approved(self):
        event = create_event(10,30, approved=True)
        response = self.client.get("/events/")
        self.assertQuerysetEqual(
            response.context["cur_events"],
            [],
        )
        self.assertQuerysetEqual(
            response.context["future_events"],
            [event],
        )

    def test_current_events(self):
        event = create_event(-10,30)
        response = self.client.get("/events/")
        self.assertQuerysetEqual(
            response.context["cur_events"],
            [],
        )
        self.assertQuerysetEqual(
            response.context["future_events"],
            [],
        )

    def test_current_events_approved(self):
        event = create_event(-10,30, approved=True)
        response = self.client.get("/events/")
        self.assertQuerysetEqual(
            response.context["cur_events"],
            [event],
        )
        self.assertQuerysetEqual(
            response.context["future_events"],
            [],
        )


