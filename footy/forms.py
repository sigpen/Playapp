from django import forms
from django.contrib.auth.models import User
from django.contrib.gis import forms as geoforms
from django.contrib.gis.geos import Point
from django.forms.models import inlineformset_factory

from footy.models import Event, Location, UserProfile

unit_srid = 4326


# Django's auth user model field
class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=200, widget=forms.PasswordInput())
    phone_number = forms.CharField(max_length=200, required=False)

    # Hashing password
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
        )


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'register-input'}))
    password = forms.CharField(max_length=300, widget=forms.PasswordInput(attrs={'class': 'register-input'}))


# TODO Search for users.
# Adding class to the input fields.
class EventForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'register-input'}))
    extras = forms.CharField(widget=forms.TextInput(attrs={'class': 'register-input'}))
    users = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(attrs={'class': 'player-list'}),
        queryset=UserProfile.objects.all(),
        label=''
    )

    class Meta:
        model = Event
        fields = (
            'users',
            'location',
            'title',
            'time',
            'extras',
        )


class LocationForm(forms.ModelForm):
    lng = forms.CharField(widget=forms.TextInput(attrs={'class': 'hidden'}), label='')
    lat = forms.CharField(widget=forms.TextInput(attrs={'class': 'hidden'}), label='')
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'register-input'}), label='')

    class Meta:
        model = Location
        exclude = (
            'url',
            'point',
        )