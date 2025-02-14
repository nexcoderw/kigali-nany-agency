from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import *

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom UserAdmin for managing User model in Django admin.
    """

    # Display these fields in the admin list view
    list_display = (
        'email',
        'name',
        'phone_number',
        'role',
        'is_active',
        'is_staff',
        'created_at',
        'updated_at',
        'image_thumbnail',
    )

    # Fields to search by
    search_fields = ('email', 'name', 'phone_number')

    # Filters for the sidebar
    list_filter = ('role', 'is_active', 'is_staff', 'created_at', 'updated_at')

    # Ordering of the list view
    ordering = ('email',)

    # Read-only fields in the admin detail view
    readonly_fields = ('slug', 'created_at', 'updated_at', 'image_thumbnail_display')

    # Fieldsets to organize fields in the admin detail view
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        (_('Personal Info'), {
            'fields': ('name', 'phone_number', 'image', 'image_thumbnail_display', 'slug')
        }),
        (_('Permissions'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Important Dates'), {
            'fields': ('last_login', 'created_at', 'updated_at')
        }),
    )

    # Fieldsets for the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone_number', 'password1', 'password2', 'role', 'is_active', 'is_staff'),
        }),
    )

    # Display image thumbnail in the list view
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', obj.image.url)
        return '-'
    image_thumbnail.short_description = 'Image'

    # Display image thumbnail in the detail view
    def image_thumbnail_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="150" style="object-fit: cover; border-radius: 50%;" />', obj.image.url)
        return '-'
    image_thumbnail_display.short_description = 'Profile Image'

    # Override to ensure proper handling of password hashing
    def save_model(self, request, obj, form, change):
        if change:
            obj.save()
        else:
            # When creating a new user, set the password properly
            obj.set_password(form.cleaned_data.get('password1'))
            obj.save()

    # Add custom validation or modifications if necessary
    def formfield_for_dbfield(self, db_field, **kwargs):
        return super().formfield_for_dbfield(db_field, **kwargs)

    # Add actions if necessary
    actions = ['make_active', 'make_inactive']

    @admin.action(description='Mark selected users as active')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Mark selected users as inactive')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
