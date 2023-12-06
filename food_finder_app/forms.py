from django import forms
from .models import Event
from address.forms import AddressField
from geopy.geocoders import GoogleV3
from django.conf import settings
from django import forms
from datetime import datetime


class EventForm(forms.ModelForm):
    CHOICES = (
        ('1', 'First Years'),
        ('2', 'Second Years'),
        ('3', 'Third Years'),
        ('4', 'Fourth Years'),
        ('5', 'Graduate Students'),
    )
    address = AddressField()
    available_to_years = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'horizontal_choice'}),
        choices=CHOICES,
    )
    # available_to_years = forms.CharField(max_length=6, choices=CHOICES, default='1')
    class Meta:
        model = Event
        fields = ['event_title', 'event_description', 'available_to_years', 'event_start_date', 'event_end_date', 'address']
        # event_title = forms.CharField(label='event_title', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
        widgets = {
            'event_title': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 1}),
            'event_description': forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 3}),
            'event_start_date': forms.DateInput(attrs={'type':'datetime-local'}),
            'event_end_date': forms.DateInput(attrs={'type':'datetime-local'}),
        }

    def save(self, commit=True):
        instance = super(EventForm, self).save(commit=False)


        geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)

        # Calculate the value of calculated_field based on form inputs
        location = geolocator.geocode(self.cleaned_data['address'])
        
        if location is None:
            self.add_error('address', 'Invalid address')
            return None

        instance.event_lattitude = location.latitude
        instance.event_longitude = location.longitude

        instance.available_to = ','.join(self.cleaned_data['available_to_years'])

        # print(self.cleaned_data['event_title'])
        if len(self.cleaned_data['event_title']) > 40:
            self.add_error('event_title', 'Event title is too long')
            return None
        
        if len(self.cleaned_data['event_description']) > 1000:
            self.add_error('event_description', 'Event description is too long')
            return None
        # commit = False

        if commit:
            instance.save()

        return instance