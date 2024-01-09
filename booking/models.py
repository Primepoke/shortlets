from django.db import models

from property.models import Property, RenterProfile
# Create your models here.



class Booking(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    renter = models.ForeignKey(RenterProfile, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)

    # Additional fields as needed
    # Calculate number of days
    def get_number_of_days(self):
        return (self.check_out_date - self.check_in_date).days
    
    # Calculate total amount
    def get_total_price(self):
        self.total_price = self.property.price_per_night * self.get_number_of_days()
        # Save the model to persist the total price
        self.save()

    def __str__(self):
        return f"{self.renter.username}'s Booking for {self.property.title}"
