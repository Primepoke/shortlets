from django.urls import path
from . import views

urlpatterns = [
    path('booking/<int:property_id>', views.create_booking, name='create_booking'),
    path('property/check_availability/<int:property_id>', views.check_availability, name='check_availability'),
    path('booking/login_check', views.login_check, name='login_check'),
    path('booking/confirm_booking/<int:booking_id>', views.confirm_booking, name='confirm_booking'),
]