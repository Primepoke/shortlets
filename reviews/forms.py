from django import forms

from .models import Review, Response

class RenterReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'rating', 'comment', 'review_image']


class ManagerResponseForm(forms.ModelForm):  
    is_manager_response_visible = forms.BooleanField(label='Do you want this response to be public?')

    class Meta:
        model = Response
        fields = ['response', 'is_manager_response_visible']