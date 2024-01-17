from django import forms

class ConfirmBookingForm(forms.Form):
    email = forms.EmailField()