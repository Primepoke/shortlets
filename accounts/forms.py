from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import ManagerProfile, RenterProfile, User

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget



class UserForm(UserCreationForm):
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='NG', attrs={'class': 'form-control'}), required=True)
    registration_type = forms.ChoiceField(choices=[('manager', 'Manager'), ('renter', 'Renter')],
                                          widget=forms.RadioSelect, label='Choose registration type: (Are you renting? Or Do you want to list properties for rental?)',
                                          required=False)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'age', 'email', 'phone_number', 'gender', 'registration_type']
        

    # Explicitly mark all other fields as required
    # first_name = forms.CharField(required=True)
    # last_name = forms.CharField(required=True)
    # username = forms.CharField(required=True)
    # email = forms.EmailField(required=True)
    # gender = forms.CharField(required=True)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Mark all fields as required
        # for field_name, field in self.fields.items():
        #     field.required = True

        # Explicitly mark additional fields as required
        for field_name in ['first_name', 'last_name', 'username', 'age', 'email', 'gender']:
            self.fields[field_name].required = True


class ManagerRegistrationForm(forms.ModelForm):

    class Meta:
        model = ManagerProfile
        fields = ['company_name', 'contact_email', 'image', 'about', 'twitter', 'linkedIn', 'facebook', 'instagram', 'tiktok']


class RenterRegistrationForm(forms.ModelForm):

    class Meta:
        model = RenterProfile
        fields = ['occupation', 'job_title', 'emergency_contact_name', 'emergency_contact_phone', 'preferred_contact_method', 'image', 'twitter', 'linkedIn', 'facebook', 'instagram', 'tiktok']




# FORMS FOR EDITING USER/PROFILE DETAILS

class UserEditForm(UserChangeForm):
    password = None #Removes the password field
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'age', 'email', 'phone_number', 'gender']


class ManagerProfileEditForm(forms.ModelForm):
    class Meta:
        model = ManagerProfile
        fields = ['company_name', 'contact_email', 'about', 'image']


class RenterProfileEditForm(forms.ModelForm):
    class Meta:
        model = RenterProfile
        fields = ['occupation', 'job_title', 'emergency_contact_name', 'emergency_contact_phone', 'preferred_contact_method', 'image']