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
