from django.contrib import admin
from .models import User, NannyProfile, Booking, Review

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_nanny', 'is_client')
    list_filter = ('is_staff', 'is_superuser', 'is_nanny', 'is_client')
    search_fields = ('username', 'first_name', 'last_name', 'email')

class NannyProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'contact_number', 'hourly_rate', 'experience_years')
    list_filter = ('experience_years',)
    search_fields = ('user__username', 'user__email', 'full_name')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'nanny', 'start_date', 'end_date', 'status', 'payment_status')
    list_filter = ('status', 'payment_status', 'start_date', 'end_date')
    search_fields = ('client__username', 'nanny__username', 'start_date')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('nanny', 'client', 'rating', 'date_posted')
    list_filter = ('rating', 'date_posted')
    search_fields = ('nanny__username', 'client__username', 'rating')

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(NannyProfile, NannyProfileAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Review, ReviewAdmin)
