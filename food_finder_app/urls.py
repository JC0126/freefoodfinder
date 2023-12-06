from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView
from . import views
from .views import EventDetailView

app_name = "food_finder_app"
urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name = "index"),
    path("accounts/", include("allauth.urls")),
    path("logout", LogoutView.as_view()),
    path("map", views.map, name="map"),
    path("events/", views.events, name="events"),
    path("create_event/", views.create_event, name="create-event"),
    path("approval/", views.approval, name = "approval"),
    path('events/details/<int:pk>', EventDetailView.as_view(), name="event-detail"),
]
