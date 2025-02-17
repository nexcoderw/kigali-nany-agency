from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from base.models import JobPosting, JobCategory, JobStatus, JobApplication
from django.contrib.auth import get_user_model

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    """
    Custom JobPostingAdmin for managing job postings in Django admin.
    """
    list_display = (
        'title',
        'client',
        'category_display',
        'status_display',
        'salary',
        'location',
        'start_date',
        'end_date',
        'created_at',
        'updated_at',
        'slug',
    )

    search_fields = ('title', 'client__email', 'location')
    list_filter = ('category', 'status', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('slug', 'created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'category', 'status', 'salary', 'location', 'start_date', 'end_date', 'client')
        }),
        (_('Dates'), {
            'fields': ('created_at', 'updated_at')
        }),
        (_('Other Information'), {
            'fields': ('slug',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('title', 'description', 'category', 'status', 'salary', 'location', 'start_date', 'end_date', 'client'),
        }),
    )

    def category_display(self, obj):
        return obj.get_category_display()
    category_display.short_description = 'Category'

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = 'Status'

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = obj.generate_unique_slug()
        super().save_model(request, obj, form, change)

    actions = ['make_open', 'make_closed', 'make_pending', 'make_in_progress']

    @admin.action(description='Mark selected jobs as open')
    def make_open(self, request, queryset):
        queryset.update(status=JobStatus.OPEN)

    @admin.action(description='Mark selected jobs as closed')
    def make_closed(self, request, queryset):
        queryset.update(status=JobStatus.CLOSED)

    @admin.action(description='Mark selected jobs as pending')
    def make_pending(self, request, queryset):
        queryset.update(status=JobStatus.PENDING)

    @admin.action(description='Mark selected jobs as in progress')
    def make_in_progress(self, request, queryset):
        queryset.update(status=JobStatus.IN_PROGRESS)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['client'].queryset = get_user_model().objects.filter(role='Client')
        return form


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    """
    Custom JobApplicationAdmin for managing job applications in Django admin.
    """
    list_display = (
        'nanny_name',
        'job_title',
        'status_display',
        'applied_at',
        'updated_at',
    )

    search_fields = ('nanny__email', 'job__title', 'status')
    list_filter = ('status', 'applied_at', 'updated_at')
    ordering = ('-applied_at',)
    readonly_fields = ('applied_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('nanny', 'job', 'experience', 'availability', 'cover_letter', 'status')
        }),
        (_('Dates'), {
            'fields': ('applied_at', 'updated_at')
        }),
    )

    def nanny_name(self, obj):
        return obj.nanny.name
    nanny_name.short_description = 'Nanny Name'

    def job_title(self, obj):
        return obj.job.title
    job_title.short_description = 'Job Title'

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = 'Status'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

