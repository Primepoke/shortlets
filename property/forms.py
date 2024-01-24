from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Property


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'video', 'video2', 'image', 'image2', 'image3', 'image4', 'image5', 'description', 'address', 'city', 'state', 'zip_code', 'country', 'price_per_night', 'parlours', 'bedrooms', 'bathrooms', 'guests_capacity', 'features', 'is_available']
        widgets = {
            'features': forms.CheckboxSelectMultiple,
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['video'].required = False
        self.fields['video2'].required = False
        self.fields['image'].required = False
        self.fields['image2'].required = False
        self.fields['image3'].required = False
        self.fields['image4'].required = False
        self.fields['image5'].required = False

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            allowed_extensions = ['mp4', 'avi', 'mkv', 'mov', 'wmv']  # Add more if needed
            file_extension = video.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError(_('Invalid file type. Please upload a valid video file.'))
        return video

    def clean_video2(self):
        video2 = self.cleaned_data.get('video2')
        if video2:
            allowed_extensions = ['mp4', 'avi', 'mkv', 'mov', 'wmv']  # Add more if needed
            file_extension = video2.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError(_('Invalid file type. Please upload a valid video file.'))
        return video2

    def clean(self):
        cleaned_data = super().clean()
        video = cleaned_data.get('video')
        video2 = cleaned_data.get('video2')
        image = cleaned_data.get('image')
        image2 = cleaned_data.get('image2')
        image3 = cleaned_data.get('image3')
        image4 = cleaned_data.get('image4')
        image5 = cleaned_data.get('image5')

        if not video and not video2 and not image and not image2 and not image3 and not image4 and not image5:
            raise forms.ValidationError('Please provide either a video or pictures of the apartment or both')
        
        return cleaned_data


