from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profile/manager', views.manager_registration, name='manager_registration'),
    path('profile/renter', views.renter_registration, name='renter_registration'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>', views.profile, name='profile'),
    # path('profile/manager/<str:username>', views.manager_profile, name='manager_profile'),
    # path('profile/renter/<str:username>', views.renter_profile, name='renter_profile'),
    path('property/new_listing', views.new_listing, name='new_listing'),
    path('property/listing/<int:listing_id>', views.listing_details, name='listing_details'),
]