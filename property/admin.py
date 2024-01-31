from django.contrib import admin

from .models import Feature, Property, PropertyType

# Register your models here.

admin.site.register(Feature)
admin.site.register(Property)
admin.site.register(PropertyType)
