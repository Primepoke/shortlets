from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import ManagerProfile, RenterProfile, User, Property


from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class UserForm(UserCreationForm):
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='NG', attrs={'class': 'form-control'}), required=True)
    registration_type = forms.ChoiceField(choices=[('manager', 'Manager'), ('renter', 'Renter')],
                                          widget=forms.RadioSelect, label='Choose registration type: (Are you renting? Or Do you want to list properties for rental?)',)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'gender', 'registration_type']
        

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
        for field_name in ['first_name', 'last_name', 'username', 'email', 'gender']:
            self.fields[field_name].required = True


class ManagerRegistrationForm(forms.ModelForm):

    class Meta:
        model = ManagerProfile
        fields = ['company_name', 'contact_email', 'picture']


class RenterRegistrationForm(forms.ModelForm):

    class Meta:
        model = RenterProfile
        fields = ['emergency_contact_name', 'emergency_contact_phone', 'preferred_contact_method', 'picture']

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'video', 'picture', 'description', 'address', 'city', 'state', 'zip_code', 'country', 'price_per_night', 'parlours', 'bedrooms', 'bathrooms', 'guests_capacity', 'features', 'is_available']
        widgets = {
            'features': forms.CheckboxSelectMultiple,
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['video'].required = False
        self.fields['picture'].required = False

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            allowed_extensions = ['mp4', 'avi', 'mkv', 'mov', 'wmv']  # Add more if needed
            file_extension = video.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError(_('Invalid file type. Please upload a valid video file.'))
        return video

    def clean(self):
        cleaned_data = super().clean()
        video = cleaned_data.get('video')
        picture = cleaned_data.get('picture')

        if not video and not picture:
            raise forms.ValidationError('Please provide either a video or pictures of the apartment or both')
        
        return cleaned_data
