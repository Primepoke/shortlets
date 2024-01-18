from django.contrib import admin

from .models import Payment, UserWallet

# Register your models here.
admin.site.register(Payment)
admin.site.register(UserWallet)