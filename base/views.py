from base.forms import *
from base.models import *
from django.db.models import Q
from django.http import Http404
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    return render(request, 'pages/index.html')

def getJobs(request):
    jobs = JobPosting.objects.all().order_by('-created_at')

    # --- Filtering ---
    category = request.GET.get('category')
    if category:
        jobs = jobs.filter(category__iexact=category)

    status = request.GET.get('status')
    if status:
        jobs = jobs.filter(status__iexact=status)

    location = request.GET.get('location')
    if location:
        jobs = jobs.filter(location__icontains=location)

    salary_min = request.GET.get('salary_min')
    if salary_min:
        jobs = jobs.filter(salary__gte=salary_min)

    salary_max = request.GET.get('salary_max')
    if salary_max:
        jobs = jobs.filter(salary__lte=salary_max)

    # --- Sorting ---
    sort = request.GET.get('sort')
    if sort:
        if sort.lower() == 'oldest':
            jobs = jobs.order_by('created_at')
        elif sort.lower() == 'newest':
            jobs = jobs.order_by('-created_at')
        else:
            jobs = jobs.order_by('-created_at')

    # --- Pagination ---
    limit = request.GET.get('limit', 12)
    try:
        limit = int(limit)
    except ValueError:
        limit = 12
    paginator = Paginator(jobs, limit)
    page = request.GET.get('page')
    try:
        jobs_page = paginator.page(page)
    except PageNotAnInteger:
        jobs_page = paginator.page(1)
    except EmptyPage:
        jobs_page = paginator.page(paginator.num_pages)

    # --- Dynamic Filter Options ---
    job_categories = JobCategory.choices
    job_statuses = JobStatus.choices

    context = {
        'jobs': jobs_page,
        'job_categories': job_categories,
        'job_statuses': job_statuses,
        'filter_params': request.GET,
        'jobs_count': paginator.count,
        'paginator': paginator,
        'page_obj': jobs_page,
    }

    return render(request, 'pages/jobs/index.html', context)

def showJobDetails(request):
    pass

def dashboard(request):
    return render(request, 'pages/user/dashboard.html')

@login_required
def getJobListings(request):
    """
    Display the list of job postings with filtering, sorting, and pagination.
    """
    # Fetch filter criteria from the request
    status_filter = request.GET.get('status')
    sort_by = request.GET.get('sort', 'newest')

    # Filter the job postings by client
    job_postings = JobPosting.objects.filter(client=request.user)

    # Apply status filter if provided
    if status_filter:
        job_postings = job_postings.filter(status=status_filter)

    # Apply sorting
    if sort_by == 'oldest':
        job_postings = job_postings.order_by('created_at')
    else:
        job_postings = job_postings.order_by('-created_at')

    # Set up pagination
    paginator = Paginator(job_postings, 10)  # Show 10 job postings per page
    page_number = request.GET.get('page')  # Get the page number from the query params
    page_obj = paginator.get_page(page_number)

    context = {
        'job_postings': page_obj,
        'status_filter': status_filter,
        'sort_by': sort_by,
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