from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_nanny = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

class NannyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nanny_profile')
    full_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    experience_years = models.IntegerField(default=0)
    certifications = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.full_name
