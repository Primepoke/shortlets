from django import forms


from .models import Feedback, IncidentReport

class LeaveFeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields =['title', 'feedback_description']


class IncidentReportForm(forms.ModelForm):

    class Meta:
        model = IncidentReport
        fields =['title', 'incident_date', 'incident_description', 'image']