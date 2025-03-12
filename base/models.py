import os
import random
from account.models import *
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

class JobCategory(models.TextChoices):
    CHILD_CARE = 'child_care', _('Child Care')
    ELDERLY_CARE = 'elderly_care', _('Elderly Care')
    SICK_CARE = 'sick_care', _('Sick Care')
    DISABILITY_CARE = 'disability_care', _('Disability Care')
    HOUSEKEEPING = 'housekeeping', _('Housekeeping')
    PET_CARE = 'pet_care', _('Pet Care')
    NANNY_SHARE = 'nanny_share', _('Nanny Share')
    HOUSE_NANNY = 'house_nanny', _('House Nanny')
    LIVE_IN_NANNY = 'live_in_nanny', _('Live-in Nanny')
    NIGHT_NANNY = 'night_nanny', _('Night Nanny')
    SPECIAL_NEEDS_CARE = 'special_needs_care', _('Special Needs Care')
    SENIOR_CARE = 'senior_care', _('Senior Care')

class JobStatus(models.TextChoices):
    OPEN = 'open', _('Open')
    CLOSED = 'closed', _('Closed')
    PENDING = 'pending', _('Pending')
    IN_PROGRESS = 'in_progress', _('In Progress')

class JobPosting(models.Model):
    client = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='job_postings',
        limit_choices_to={'role': 'Client'}
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=JobCategory.choices)
    status = models.CharField(max_length=50, choices=JobStatus.choices, default=JobStatus.OPEN)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate slug based on the title and update it if the title changes
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1
        while JobPosting.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def __str__(self):
        return f"{self.title} - {self.client.email}"

    class Meta:
        verbose_name = _('Job Posting')
        verbose_name_plural = _('Job Postings')

class ApplicationStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    ACCEPTED = 'accepted', _('Accepted')
    REJECTED = 'rejected', _('Rejected')

class JobApplication(models.Model):
    nanny = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'Nanny'}, related_name='applications'
    )
    job = models.ForeignKey(
        JobPosting, on_delete=models.CASCADE, related_name='applications'
    )
    experience = models.TextField(null=True, blank=True, help_text=_('Describe your experience relevant to this job.'))
    availability = models.DateField(null=True, blank=True, help_text=_('Specify your availability for the job.'))
    cover_letter = models.TextField(null=True, blank=True, help_text=_('Provide any additional information or comments.'))
    status = models.CharField(
        max_length=50, choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Application for {self.job.title} by {self.nanny.name}"

    class Meta:
        verbose_name = _('Job Application')
        verbose_name_plural = _('Job Applications')
        unique_together = ('nanny', 'job')

class HireApplication(models.Model):
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'Client'}, related_name='hire_applications'
    )
    nanny = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'Nanny'}, related_name='received_applications'
    )
    job_posting = models.ForeignKey(
        JobPosting, on_delete=models.SET_NULL, null=True, blank=True, related_name='hire_applications'
    )
    job_title = models.CharField(max_length=255, help_text='The title of the job the client is offering')
    description = models.TextField(help_text='Detailed description of the job')
    expected_start_date = models.DateField(help_text='Expected date for the nanny to start the job')
    expected_end_date = models.DateField(help_text='Expected date for the nanny to finish the job')
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, help_text='Expected salary for the nanny')
    work_schedule = models.TextField(help_text='Detailed work schedule for the nanny')
    additional_requirements = models.TextField(null=True, blank=True, help_text='Any additional requirements or comments from the client')
    status = models.CharField(
        max_length=50,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending',
        help_text='The current status of the application'
    )
    applied_at = models.DateTimeField(default=timezone.now, help_text='The time the nanny was applied to')
    updated_at = models.DateTimeField(auto_now=True, help_text='The time the application was last updated')

    def __str__(self):
        return f"Hire application from {self.client.name} to {self.nanny.name} for {self.job_title}"

    class Meta:
        verbose_name = 'Hire Application'
        verbose_name_plural = 'Hire Applications'
        unique_together = ('client', 'nanny', 'job_posting')

class NannyProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='nanny_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True, help_text=_('Brief biography of the nanny'))
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    certifications = models.TextField(null=True, blank=True, help_text=_('Certifications or courses completed'))
    languages_spoken = models.TextField(null=True, blank=True, help_text=_('Languages spoken by the nanny'))
    previous_employers = models.TextField(null=True, blank=True, help_text=_('Details of previous employers'))
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text=_('Hourly rate for services'))
    preferred_working_hours = models.TextField(null=True, blank=True, help_text=_('Preferred working hours'))
    availability_notes = models.TextField(null=True, blank=True, help_text=_('Any additional availability notes'))
    
    def __str__(self):
        return f"Nanny Profile for {self.user.name}"

    class Meta:
        verbose_name = 'Nanny Profile'
        verbose_name_plural = 'Nanny Profiles'

class ClientProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='client_profile')
    company_name = models.CharField(max_length=255, null=True, blank=True, help_text=_('Name of the company hiring the nanny'))
    company_description = models.TextField(null=True, blank=True, help_text=_('Brief description of the company'))
    address = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"Client Profile for {self.user.name}"

    class Meta:
        verbose_name = 'Client Profile'
        verbose_name_plural = 'Client Profiles'

def team_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    return f'team/member_{slugify(instance.name)}_{timestamp}.png'

class Team(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    image = ProcessedImageField(
        upload_to=team_image_path,
        processors=[ResizeToFill(1333, 1694)],
        format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def _generate_unique_slug(self):
        """Generate a unique slug based on the name."""
        base_slug = slugify(self.name)
        slug = base_slug
        while Team.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        return slug
    
    def save(self, *args, **kwargs):
        # Only update slug if name has changed
        if self.pk:  # Check if the instance already exists
            original = Team.objects.get(pk=self.pk)
            if self.name != original.name:
                self.slug = self._generate_unique_slug()  # Update slug only if name is changed
        elif not self.slug:  # For new objects, generate a slug
            self.slug = self._generate_unique_slug()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name if self.name else "Unnamed Team Member"
    
    class Meta:
        verbose_name_plural = "Team Members"

def logo_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    random_number = random.randint(1000, 9999)
    return f'settings/logo/{random_number}_{timestamp}{file_extension}'


class Setting(models.Model):
    logo = ProcessedImageField(
        upload_to=logo_image_path,
        # processors=[ResizeToFill(600, 600)],
        format='PNG',
        options={'quality': 90},
        null=True,
        blank=True
    )
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    second_email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Ensure only one instance of settings can exist
        if not self.pk and Setting.objects.exists():
            raise ValueError("You can only create one instance of the settings.")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return "Website Settings"
    
    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"