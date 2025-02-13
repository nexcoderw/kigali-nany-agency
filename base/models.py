from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    ROLE_CHOICES = [
        ('nanny', 'Nanny'),
        ('client', 'Client'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="user_profiles",  # Avoids conflict with 'auth.User.groups'
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="user_profiles",  # Avoids conflict with 'auth.User.user_permissions'
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class NannyProfile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="nanny_profile")
    experience = models.IntegerField(help_text="Years of experience")
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    availability = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.experience} years experience"

class ClientProfile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="client_profile")
    number_of_children = models.IntegerField(default=1, help_text="Number of children")
    special_requirements = models.TextField(blank=True, null=True, help_text="Any special needs or requirements")

    def __str__(self):
        return f"{self.user.username} - {self.number_of_children} children"



