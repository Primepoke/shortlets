from django.contrib import admin

from .models import Booking, Feature, ManagerProfile, Property, RenterProfile, Review, User

# Register your models here.

admin.site.register(Booking)
admin.site.register(Feature)
admin.site.register(ManagerProfile)
admin.site.register(Property)
admin.site.register(RenterProfile)
admin.site.register(Review)
admin.site.register(User)