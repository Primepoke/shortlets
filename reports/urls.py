from django.urls import path

from . import views

urlpatterns = [
    path('feedback', views.leave_feedback, name='leave_feedback'),
    path('reports', views.report_incident, name='report_incident')
]