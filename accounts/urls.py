from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('manager', views.manager_registration, name='manager_registration'),
    path('renter', views.renter_registration, name='renter_registration'),
    path('edit', views.profile_edit, name='profile_edit'),
    path('<str:username>', views.profile, name='profile'),
]
