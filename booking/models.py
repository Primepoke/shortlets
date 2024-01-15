from django.db import models

from property.models import Property, RenterProfile
# Create your models here.



class Booking(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    renter = models.ForeignKey(RenterProfile, on_delete=models.CASCADE, related_name='bookings')
    check_in_datetime = models.DateTimeField()
    check_out_datetime = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    confirmation_status = models.CharField(max_length=20, choices=[('unconfirmed', 'Unconfirmed'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='unconfirmed')
    # is_confirmed = models.BooleanField(default=False)
    # is_canceled = models.BooleanField(default=False)

    # Additional fields as needed
    # Calculate number of days
    def get_stay_duration(self):
        return (self.check_out_datetime - self.check_in_datetime).days
    
    # Calculate total amount
    def get_total_price(self):
        self.total_price = self.property.price_per_night * self.get_stay_duration()
        # # Save the model to persist the total price
        # self.save()

    def __str__(self):
        return f"{self.renter.user.username}'s Booking for {self.property.title}"
    
    # confirmation status functions
    def save_unconfirmed(self):
        self.confirmation_status = 'unconfirmed'

    def save_confirmed(self):
        self.confirmation_status = 'confirmed'

    def save_canceled(self):
        self.confirmation_status = 'canceled'
