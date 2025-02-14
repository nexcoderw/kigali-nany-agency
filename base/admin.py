from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from base.models import JobPosting, JobCategory, JobStatus

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    """
    Custom JobPostingAdmin for managing job postings in Django admin.
    """

    # Display these fields in the admin list view
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

    # Fields to search by
    search_fields = ('title', 'client__email', 'location')

    # Filters for the sidebar
    list_filter = ('category', 'status', 'created_at', 'updated_at')

    # Ordering of the list view
    ordering = ('-created_at',)

    # Read-only fields in the admin detail view
    readonly_fields = ('slug', 'created_at', 'updated_at')

    # Fieldsets to organize fields in the admin detail view
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

    # Fieldsets for the add JobPosting form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('title', 'description', 'category', 'status', 'salary', 'location', 'start_date', 'end_date', 'client'),
        }),
    )

    # Display category in the list view as human-readable
    def category_display(self, obj):
        return obj.get_category_display()
    category_display.short_description = 'Category'

    # Display status in the list view as human-readable
    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = 'Status'

    # Override save method to ensure the slug is always unique and correctly generated
    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = obj.generate_unique_slug()
        super().save_model(request, obj, form, change)

    # Add custom actions if necessary (optional)
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
