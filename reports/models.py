from django.db import models

# Create your models here.

class Feedback(models.Model):
    title = models.CharField(max_length=50)
    feedback_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    feedback_by = models.CharField(max_length=50, default='Anonymous User')
    # Add other feedback-related fields here

class IncidentReport(models.Model):
    title = models.CharField(max_length=50)
    property = models.ForeignKey('property.Property', on_delete=models.CASCADE, null=True, blank=True)
    incident_date = models.DateField(help_text='Date incident happened.')
    incident_description = models.TextField()
    report_by = models.CharField(max_length=50, default='Anonymous User')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True)
    # Add other incident-related fields here
