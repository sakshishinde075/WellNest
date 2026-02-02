from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser."""
    
    # Additional fields for user profile
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    
    # Privacy and consent fields
    privacy_consent = models.BooleanField(default=False)
    data_processing_consent = models.BooleanField(default=False)
    marketing_consent = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
