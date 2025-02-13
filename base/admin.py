from django.contrib import admin
from .models import UserProfile, NannyProfile, ClientProfile, Booking

admin.site.register(UserProfile)
admin.site.register(NannyProfile)
admin.site.register(ClientProfile)
admin.site.register(Booking)
