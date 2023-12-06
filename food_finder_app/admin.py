from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from .models import Event
from django.utils.translation import gettext_lazy as _

from food_finder_app.models import CustomGroup


# from food_finder_app.models import CustomGroup

# Register your models here.
# admin.site.unregister(Group)


@admin.register(CustomGroup)
class CustomGroupAdmin(GroupAdmin):
    fieldsets = None


admin.site.register(Event)
