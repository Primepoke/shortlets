from django.db import models

from accounts.models import RenterProfile
from property.models import Property
# Create your models here.

class Review(models.Model):
    # Renter's review
    title  = models.CharField(max_length=255, blank=True, null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    renter = models.ForeignKey(RenterProfile, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    review_image = models.ImageField(upload_to='review_images/', blank=True, null=True)
    helpful_votes = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('pending', 'Pending'), ('archived', 'Archived')], default='active')

    # Additional fields as needed

    def __str__(self):
        return f"{self.renter.user.username}'s Review for {self.property.title}"

class Response(models.Model):
    # Manager's response to the review
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='manager_response')
    response = models.TextField(blank=True, null=True)
    response_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_manager_response_visible = models.BooleanField(default=False)


    # Additional fields as needed

    def __str__(self):
        return f"{self.review.property.property_manager.user.username}'s Response to {self.review.renter.user.username}'s Review on {self.review.property.title}"