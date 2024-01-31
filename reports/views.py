from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from.forms import IncidentReport, LeaveFeedbackForm

from accounts.models import RenterProfile

# Create your views here.


def leave_feedback(request):
    user = request.user

    if request.method == 'POST':
        form = LeaveFeedbackForm(request.POST)

        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.feedback_by = user
            feedback.save()

            messages.suucess(request, "Thanks for submitting your feedback. We'll attend to it speedily")
            return redirect(reverse('index'))
    
    form = LeaveFeedbackForm()

    return render(request, 'reports/feeback.html', {'form': form})


@login_required
def report_incident(request):
    user = request.user

    if request.method == 'POST':
        form = IncidentReport(request.POST)

        if form.is_valid():
            report = form.save(commit=False)
            report.report_by = user
            report.save()

            messages.suucess(request, "Your report was successfully submitted. We'll attend to it speedily")
            return redirect(reverse('index'))
        
    if hasattr(user, 'renter'):
        profile = get_object_or_404(RenterProfile, user=user)
        bookings = profile.bookings.all()
        properties = set(booking.property for booking in bookings)
        
        if properties:
            form = IncidentReport(initial={'property': [property.title for property in properties]})
        else:
            form = IncidentReport()
    
    return render(request, 'reports/reports.html', {'form': form})