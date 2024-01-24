from django.contrib import admin

from .models import ManagerProfile, RenterProfile, User

# Register your models here.


admin.site.register(ManagerProfile)
admin.site.register(RenterProfile)
admin.site.register(User)