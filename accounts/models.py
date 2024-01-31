from django.db import models

from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class User(AbstractUser):
    age = models.CharField(max_length=20, choices=[('18-30', '18-30'), ('31-45', '31-45'), ('46-60', '46-60'), ('61+', '61 and above')], default='31-45', help_text="Select age bracket")
    phone_number = PhoneNumberField(help_text="Enter your phone number")
    gender = models.CharField(max_length=20, choices=[('male', 'Male'), ('female', 'Female')], default='male', help_text="Select your gender")



class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="manager")
    company_name = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(help_text="Contact email address")
    about = models.TextField(blank=True, null=True, help_text="Tell us about yourself.")
    properties_managed = models.ManyToManyField('property.Property', related_name='managers', blank=True)
    image = models.ImageField(upload_to='managers_pictures/', blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedIn = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Manager Profile"
    
    


class RenterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='renter')
    occupation = models.CharField(max_length=255, help_text="Occupation")
    job_title = models.CharField(max_length=255, help_text="Occupation")
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True, help_text="Emergency contact name")
    emergency_contact_phone = PhoneNumberField(blank=True, null=True, help_text="Emergency contact phone number")
    preferred_contact_method = models.CharField(max_length=20, choices=[('phone', 'Phone'), ('email', 'Email')], default='phone', help_text="Preferred contact method")
    image = models.ImageField(upload_to='renters_pictures/', blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedIn = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)
    # id card
    
    


    def __str__(self):
        return f"{self.user.username}'s Renter Profile"
