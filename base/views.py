from base.forms import *
from base.models import *
from django.http import Http404
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

def home(request):
    return render(request, 'pages/index.html')

def dashboard(request):
    return render(request, 'pages/user/dashboard.html')

@login_required
def getJobListings(request):
    """
    Display the list of job postings.
    """
    jobListing = JobPosting.objects.filter(client=request.user).order_by('-created_at')

    context = {
        'jobListing': jobListing
    }

    return render(request, 'pages/user/listings/index.html', context)

@login_required
def addJobListing(request):
    """
    Add a new job listing.
    """
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.client = request.user
            job.save()
            messages.success(request, _('Your job listing has been successfully created.'))
            return redirect(reverse('base:getJobListings'))
        else:
            messages.error(request, _('Please fix the errors below.'))
    else:
        form = JobPostingForm()

    context = {
        'form': form
    }

    return render(request, 'pages/user/listings/create.html', context)

@login_required
def editJobListing(request, slug):
    """
    Edit an existing job listing.
    """
    job = get_object_or_404(JobPosting, slug=slug, client=request.user)
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your job listing has been updated.'))
            return redirect(reverse('base:getJobListings'))
        else:
            messages.error(request, _('Please fix the errors below.'))
    else:
        form = JobPostingForm(instance=job)

    context = {
        'form': form,
        'job': job
    }

    return render(request, 'pages/user/listings/edit.html', context)

@login_required
def deleteJobListing(request, slug):
    """
    Delete a job listing.
    """
    try:
        job = JobPosting.objects.get(slug=slug, client=request.user)
        job.delete()
        messages.success(request, _('Your job listing has been deleted.'))
    except JobPosting.DoesNotExist:
        raise Http404(_('Job listing not found.'))

    return redirect(reverse('base:getJobListings'))