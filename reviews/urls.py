from django.urls import path

from . import views

urlpatterns = [
    path('property/<int:property_id>', views.create_review, name='create_review'),
    path('response/<int:review_id>', views.respond_to_review, name='respond_to_review'),
]