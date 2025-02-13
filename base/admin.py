from django.contrib import admin
from .models import UserProfile, NannyProfile

admin.site.register(UserProfile)
admin.site.register(NannyProfile)
