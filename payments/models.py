from django.db import models
# from django.utils import timezone
import secrets
from .paystack import Paystack

from accounts.models import ManagerProfile
from booking.models import Booking

# Create your models here.

class UserWallet(models.Model):
    manager_profile = models.OneToOneField(ManagerProfile, on_delete=models.CASCADE, null=True, related_name='wallet')
    currency = models.CharField(max_length=50, default='NGN')
    balance = models.PositiveIntegerField(default=0)
    # created_at = models.DateTimeField(default=timezone.now, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    bank_name = models.CharField(max_length=50, default='ABC')
    account_number = models.CharField(max_length=50, default='0000000000')

    def __str__(self):
        return f"Wallet for {self.manager_profile.user.username}"


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"Payment: {self.amount}"
    
    def save(self, *args, **kwargs):
        if not self.ref:
            while True:
                ref = secrets.token_urlsafe(50)
                if not Payment.objects.filter(ref=ref).exists():
                    self.ref = ref
                    break

        super().save(*args, **kwargs)


    def amount_value(self):
        return int(self.amount) * 100

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False