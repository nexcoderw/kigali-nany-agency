import os
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from account.managers import CustomUserManager  # Ensure your custom manager is imported

def user_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return f'profile_images/user_{slugify(instance.slug)}_{instance.phone_number}{file_extension}'

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that supports profile images, role-based logic,
    and flexible assignment of groups via the admin.
    """
    ROLE_CHOICES = (
        ('Client', 'Client'),
        ('Nanny', 'Nanny'),
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    image = ProcessedImageField(
        upload_to=user_image_path,
        processors=[ResizeToFill(720, 720)],
        format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True,
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        """
        Custom save method to handle image deletion and unique slug generation.
        """
        try:
            orig = User.objects.get(pk=self.pk)
        except User.DoesNotExist:
            orig = None

        if orig:
            # Delete previous image if it has been changed
            if orig.image and self.image != orig.image:
                orig.image.delete(save=False)
            # Regenerate slug if the user's name has changed
            if orig.name != self.name:
                self.slug = self.generate_unique_slug()
        else:
            if not self.slug:
                self.slug = self.generate_unique_slug()

        super(User, self).save(*args, **kwargs)

    def generate_unique_slug(self):
        """
        Generate a unique slug based on the user's name.
        """
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        while User.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def get_full_name(self):
        """
        Return the user's full name.
        """
        return self.name

    def get_short_name(self):
        """
        Return the user's first name if available, otherwise the email.
        """
        return self.name.split()[0] if self.name else self.email
