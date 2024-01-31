from django.contrib import admin

from .models import IncidentReport, Feedback
# Register your models here.


admin.site.register(IncidentReport)
admin.site.register(Feedback)