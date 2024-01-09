from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Booking

class BookingForm(forms.ModelForm):
    check_in_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    check_out_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date']

class AvailabilityForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class LoginCheckForm(forms.Form):
    question = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')],
                                          widget=forms.RadioSelect, label='Do you already have an account and renter profile (Are you registered as a renter)?',
                                          required=False)