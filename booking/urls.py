from django.urls import path
from . import views

urlpatterns = [
    path('booking/<int:property_id>', views.create_booking, name='create_booking'),
    path('property/check-availability/<int:property_id>', views.check_availability, name='check_availability'),
    path('booking/login-check', views.login_check, name='login_check'),
    path('booking/confirm-booking/<int:booking_id>', views.confirm_booking, name='confirm_booking'),
    path('renter/booking', views.renter_bookings_view, name='renter_bookings_view'),
    path('renter/booking/details/<int:booking_id>', views.renter_booking_details, name='renter_booking_details'),
    path('manager/booking', views.manager_bookings_view, name='manager_bookings_view'),
    path('manager/booking/details/<int:booking_id>', views.manager_booking_details, name='manager_booking_details'),
]