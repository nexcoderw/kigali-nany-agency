
from base.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'base'

urlpatterns = [
    path('', home, name="home"),
    path('about', about, name="about"),
    path('services', services, name="services"),
    path('contact', contact, name="contact"),
    
    path('jobs/', getJobs, name="getJobs"),
    path('job/<slug>/', showJobDetails, name="showJobDetails"),

    path('nannies/', getNannies, name="getNannies"),
    path('nanny/<slug>/', showNanny, name="showNanny"),

    path('dashboard/', dashboard, name="dashboard"),

    # Client
    path('client/job-listings/', getJobListings, name="getJobListings"),
    path('client/job-listing/add/', addJobListing, name="addJobListing"),
    path('client/job-listing/edit/<slug:slug>/', editJobListing, name="editJobListing"),
    path('client/job-listing/delete/<slug:slug>/', deleteJobListing, name="deleteJobListing"),

    path('client/applicants/', getJobApplicants, name="getJobApplicants"),
    path('client/applicant/<id>/', getJobApplicantDetails, name="getJobApplicantDetails"),
    path('client/applicant/accept/<int:id>/', acceptApplication, name='acceptApplication'),
    path('client/applicant/reject/<int:id>/', rejectApplication, name='rejectApplication'),

    path('client/hire-applications/', getHireApplications, name="getHireApplications"),
    path('client/hire-applications/<id>/', getHireApplicationDetails, name="getHireApplicationDetails"),

    # Nanny
    path('job-applications/', getJobApplications, name="getJobApplications"),
    path('job-application/<id>/', getJobApplicationDetails, name="getJobApplicationDetails"),

    path('hire-applications/', getNannyHireApplications, name="getNannyHireApplications"),
    path('hire-applications/<id>/', getNannyHireApplicationDetails, name="getNannyHireApplicationDetails"),
    path('hire-application/accept/<int:id>/', nannyAcceptHireApplication, name='nannyAcceptHireApplication'),
    path('hire-application/reject/<int:id>/', nannyRejectHireApplication, name='nannyRejectHireApplication'),

    path('profile/', updateProfile, name='updateProfile'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)