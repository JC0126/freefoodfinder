from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.models import Group
from django.views import generic
from django import template
from django.contrib.auth.models import User
from .models import Event
from django.conf import settings
from django.contrib import messages
from .forms import EventForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import os
from django.utils import timezone
import datetime
import requests
from django.shortcuts import get_object_or_404
# https://coderbook.com/@marcus/how-to-restrict-access-with-django-permissions/#:~:text=Restrict%20access%20to%20logged%20in,function%20with%20the%20%40login_required%20decorator.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from food_finder.settings import GOOGLE_MAPS_API_KEY
from geopy.geocoders import GoogleV3


def is_admins(user):
    return user.groups.filter(name='Admins').exists()


def map(request):

    future_events = Event.objects.filter(event_start_date__gte=timezone.now()).order_by(
        "-event_start_date"
    )
    cur_events = Event.objects.filter(event_end_date__gte=timezone.now(),
                                      event_start_date__lte=timezone.now()).order_by(
        "-event_start_date"
    )
    queryset = list(cur_events)+list(future_events)
    event_list = []

    for a in queryset:
        if a.approved:
            data = {
                'lat': float(a.event_lattitude),
                'long': float(a.event_longitude),
                'name': a.event_title,
                'description':a.event_description,
                'event_id': a.id,
            }
            event_list.append(data)

    context = {
        "google_api_key": settings.GOOGLE_MAPS_API_KEY,
        "event_list": event_list
    }
    print(context)
    return render(request, "map.html", context)


def events(request):
    # https://www.vinta.com.br/blog/advanced-django-querying-sorting-events-date
    future_events = Event.objects.filter(event_start_date__gte=timezone.now(), approved=True).order_by(
        "-event_start_date"
    )
    cur_events = Event.objects.filter(event_end_date__gte=timezone.now(), event_start_date__lte=timezone.now(),approved=True).order_by(
        "-event_start_date"
    )
    print(future_events)
    print(cur_events)
    # queryset2 = Event.objects.all().order_by("-event_date")
    # print(queryset)
    # print(queryset2)
    # print(timezone.now())   
    # for i in queryset2:
    #     print(i.event_description, i.event_date)
    #     print(i.event_date > timezone.now())
    context = {"cur_events": cur_events,"future_events":future_events}


    return render(request, "events.html", context)


@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            successful = form.save()
            # return redirect("events")
            if successful:
                return HttpResponseRedirect(reverse("food_finder_app:events"))
    else:
        form = EventForm()
    return render(request, "create_event.html", {"form": form})


# https://www.youtube.com/watch?v=FzV_Py68Y_I

def approval(request):
    event_list = Event.objects.all().order_by("-event_start_date")
    if is_admins(request.user):
        if request.method == "POST":
            id_list = request.POST.getlist("boxes")

            event_list.update(approved=False)

            for id in id_list:
                Event.objects.filter(pk=int(id)).update(approved=True)
                messages.success(request, ("Event list approval has been updated"))
            return redirect("/events")
        else:
            return render(request, "admin_approval.html", {"event_list": event_list})
    else:
        messages.success(request, ("You are not allowed to view this page. You must be an admin user"))
        return redirect("/")


class EventDetailView(LoginRequiredMixin, DetailView):
    # specify the model to use
    model = Event
    template_name = "event_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        latitude = self.get_object().event_lattitude
        longitude = self.get_object().event_longitude
        geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
        coordinates = f"{latitude}, {longitude}"
        location = geolocator.reverse(coordinates)
        context["address"] = location.address if location else "Address not available"
        academic_years = self.get_object().available_to
        converted_years = convert_academic_years(academic_years)
        context["academic_years"] = converted_years
        return context

    def get_queryset(self):
        return Event.objects.all()

def convert_academic_years(academic_years):
    year_mapping = {
        1: "First Years",
        2: "Second Years",
        3: "Third Years",
        4: "Fourth Years",
        5: "Graduate Students",
    }

    years_list = [year_mapping[int(year)] for year in academic_years.split(",")]

    return ", ".join(years_list)
