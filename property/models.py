from django.db import models

from django.contrib.auth.models import AbstractUser
# from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class User(AbstractUser):
    phone_number = PhoneNumberField(help_text="Enter your phone number")
    gender = models.CharField(max_length=20, choices=[('male', 'Male'), ('female', 'Female')], default='male', help_text="Select your gender")


class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="manager")
    company_name = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(help_text="Contact email address")
    about = models.TextField(blank=True, null=True, help_text="About the property manager")
    properties_managed = models.ManyToManyField('Property', related_name='managers', blank=True)
    picture = models.ImageField(upload_to='managers_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Manager Profile"


class RenterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='renter')
    occupation = models.CharField(max_length=255, help_text="Occupation")
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True, help_text="Emergency contact name")
    emergency_contact_phone = PhoneNumberField(blank=True, null=True, help_text="Emergency contact phone number")
    preferred_contact_method = models.CharField(max_length=20, choices=[('phone', 'Phone'), ('email', 'Email')], default='phone', help_text="Preferred contact method")
    picture = models.ImageField(upload_to='renters_pictures/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Renter Profile"



class Property(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    parlours = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    guests_capacity = models.PositiveIntegerField()
    features = models.ManyToManyField('Feature', related_name='properties', blank=True)
    property_manager = models.ForeignKey(ManagerProfile, on_delete=models.CASCADE, related_name='properties')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Updated fields for optional video and picture
    video = models.FileField(upload_to='property_videos/', blank=True, null=True)
    picture = models.ImageField(upload_to='property_pictures/', blank=True, null=True)

    # Additional fields as needed

    def __str__(self):
        return self.title



class Feature(models.Model):
    name = models.CharField(max_length=255)
    number = models.PositiveIntegerField()

    # Additional fields as needed

    def __str__(self):
        return self.name


class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    renter = models.ForeignKey(RenterProfile, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Manager's response to the review
    manager_response = models.TextField(blank=True, null=True)
    manager_response_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # Additional fields as needed

    def __str__(self):
        return f"{self.renter.username}'s Review for {self.property.title}"






