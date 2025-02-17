from base.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'base'

urlpatterns = [
    path('', home, name="home"),
    path('jobs/', getJobs, name="getJobs"),
    path('job/<slug>/', showJobDetails, name="showJobDetails"),

    path('nannies/', getNannies, name="getNannies"),
    path('nanny/<slug>/', showNanny, name="showNanny"),

    path('dashboard/', dashboard, name="dashboard"),

    # Client
    path('job-listings/', getJobListings, name="getJobListings"),
    path('job-listing/add/', addJobListing, name="addJobListing"),
    path('job-listing/edit/<slug:slug>/', editJobListing, name="editJobListing"),
    path('job-listing/delete/<slug:slug>/', deleteJobListing, name="deleteJobListing"),

    path('applicants/', getJobApplicants, name="getJobApplicants"),
    path('applicant/<id>/', getJobApplicantDetails, name="getJobApplicantDetails"),
    path('applicant/accept/<int:id>/', acceptApplication, name='acceptApplication'),
    path('applicant/reject/<int:id>/', rejectApplication, name='rejectApplication'),

    # Nanny
    path('applications/', getJobApplications, name="getJobApplications"),
    path('application/<id>/', getJobApplicationDetails, name="getJobApplicationDetails"),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)