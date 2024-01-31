from django.urls import path
from . import views


urlpatterns = [
    path('search', views.property_search, name='property_search'),
]