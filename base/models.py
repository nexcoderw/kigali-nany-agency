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
