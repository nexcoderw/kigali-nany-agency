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

class Booking(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_bookings')
    nanny = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nanny_bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed')])
    payment_status = models.CharField(max_length=10, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')])

    def __str__(self):
        return f"Booking from {self.start_date} to {self.end_date} by {self.client.username}"

class Review(models.Model):
    nanny = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nanny_reviews')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    date_posted = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.client.username} for {self.nanny.username}"
