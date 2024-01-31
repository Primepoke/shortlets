from django.db import models

from accounts.models import ManagerProfile

# create your models here


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
    property_type = models.ForeignKey('PropertyType', related_name='properties', on_delete=models.CASCADE)
    property_manager = models.ForeignKey(ManagerProfile, on_delete=models.CASCADE, related_name='properties')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Updated fields for optional video and picture
    video = models.FileField(upload_to='property_videos/', blank=True, null=True)
    video2 = models.FileField(upload_to='property_videos/', blank=True, null=True)
    image = models.ImageField(upload_to='property_pictures/', blank=True, null=True)
    image2 = models.ImageField(upload_to='property_pictures/', blank=True, null=True)
    image3 = models.ImageField(upload_to='property_pictures/', blank=True, null=True)
    image4 = models.ImageField(upload_to='property_pictures/', blank=True, null=True)
    image5 = models.ImageField(upload_to='property_pictures/', blank=True, null=True)

    # Additional fields as needed

    def __str__(self):
        return self.title



class Feature(models.Model):
    name = models.CharField(max_length=255)
    number = models.PositiveIntegerField()

    # Additional fields as needed

    def __str__(self):
        return self.name


class PropertyType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name