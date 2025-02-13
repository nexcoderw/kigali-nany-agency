from base.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import sys

app_name = 'base'

urlpatterns = [
    path('', home, name="home"),
    path('about', about, name="about"),
    path('services', services, name="services"),
    path('jobs', getJobs, name="getJobs"),
    path('job/slug', showJob, name="showJob"),
    path('contact', contact, name="contact"),
    path('signup', Signup, name="signup"),
    path('login', Login, name="login"),
    path('dashboard', UserDashboard, name="dashboard"),
    path('userbookings', UserBookings, name="userbookings"),
    path('logout', Logout, name="logout"),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 