from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom UserAdmin for managing the User model.
    This admin enables assigning groups and user-specific permissions,
    along with a professional interface for image thumbnails.
    """

    # Fields displayed in the admin list view
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

    # Fieldsets for organizing fields in the admin detail view
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
            'fields': ('email', 'name', 'phone_number', 'password1', 'password2', 'role', 'is_active', 'is_staff', 'groups', 'user_permissions'),
        }),
    )

    # Enable horizontal filters for many-to-many fields
    filter_horizontal = ('groups', 'user_permissions',)

    def image_thumbnail(self, obj):
        """
        Render a small thumbnail of the user's profile image in the list view.
        """
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />',
                obj.image.url
            )
        return '-'
    image_thumbnail.short_description = 'Image'

    def image_thumbnail_display(self, obj):
        """
        Render a larger profile image in the detail view.
        """
        if obj.image:
            return format_html(
                '<img src="{}" width="150" height="150" style="object-fit: cover; border-radius: 50%;" />',
                obj.image.url
            )
        return '-'
    image_thumbnail_display.short_description = 'Profile Image'

    def save_model(self, request, obj, form, change):
        """
        Override save_model to handle password hashing on new user creation.
        """
        if not change:
            obj.set_password(form.cleaned_data.get('password1'))
        obj.save()

    # Custom admin actions for bulk updating user status
    actions = ['make_active', 'make_inactive']

    @admin.action(description='Mark selected users as active')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Mark selected users as inactive')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
