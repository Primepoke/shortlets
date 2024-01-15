from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Booking

class BookingForm(forms.ModelForm):
    check_in_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    check_out_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Booking
        fields = ['check_in_datetime', 'check_out_datetime']

    # def __init__(self, *args, **kwargs):
    #     super(BookingForm, self).__init__(*args, **kwargs)
    #     # Update the input format for datetime fields
    #     self.fields['check_in_datetime'].input_formats = ['%Y-%m-%dT%H:%M']
    #     self.fields['check_out_datetime'].input_formats = ['%Y-%m-%dT%H:%M']


class AvailabilityForm(forms.Form):
    start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

class LoginCheckForm(forms.Form):
    question = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')],
                                          widget=forms.RadioSelect, label='Do you already have an account and renter profile (Are you registered as a renter)?',
                                          required=False)