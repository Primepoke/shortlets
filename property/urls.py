from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('property/new_listing', views.new_listing, name='new_listing'),
    path('property/listing/<int:listing_id>', views.listing_details, name='listing_details'),
]