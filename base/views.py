from base.forms import *
from base.models import *
from account.models import *
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.http import Http404, JsonResponse
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

def showJobDetails(request, slug):
    job = get_object_or_404(JobPosting, slug=slug)

    # Check if the user is logged in and has the 'Nanny' role
    if request.user.is_authenticated and request.user.role == 'Nanny':
        # Check if the user has already applied for the job
        if JobApplication.objects.filter(nanny=request.user, job=job).exists():
            messages.info(request, 'You have already applied for this job.')
            return render(request, 'pages/jobs/show.html', {'job': job, 'already_applied': True})

        if request.method == 'POST':
            form = JobApplicationForm(request.POST)
            if form.is_valid():
                application = form.save(commit=False)
                application.nanny = request.user
                application.job = job
                application.save()
                messages.success(request, 'Your application has been submitted successfully.')
                return redirect(reverse('base:showJobDetails', kwargs={'slug': job.slug}))
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = JobApplicationForm()

        context = {
            'job': job,
            'form': form,
            'already_applied': False
        }
    else:
        # If the user isn't logged in or doesn't have the Nanny role, display a login redirect button
        context = {
            'job': job,
            'already_applied': False,
            'login_required': True
        }

    return render(request, 'pages/jobs/show.html', context)

def getNannies(request):
    nannies = User.objects.filter(role = 'Nanny').order_by('-created_at')

    context = {
        'nannies': nannies
    }

    return render(request, 'pages/nannies/index.html', context)

def showNanny(request, slug):
    nanny = get_object_or_404(User, slug=slug)

    # Check if the user is logged in and has the 'Client' role
    if request.user.is_authenticated and request.user.role == 'Client':
        # Check if the client has already sent a hire application to this nanny
        if HireApplication.objects.filter(client=request.user, nanny=nanny).exists():
            messages.info(request, 'You have already sent a hire application to this nanny.')
            return render(request, 'pages/nannies/show.html', {'nanny': nanny, 'already_applied': True})

        # Handle form submission
        if request.method == 'POST':
            form = HireApplicationForm(request.POST)
            if form.is_valid():
                hire_application = form.save(commit=False)
                hire_application.client = request.user  # Set the client to the logged-in user
                hire_application.nanny = nanny  # Set the nanny to the nanny whose profile is being viewed
                hire_application.save()

                messages.success(request, 'Your application to hire the nanny has been sent.')
                return redirect(reverse('base:showNanny', kwargs={'slug': nanny.slug}))
            else:
                messages.error(request, 'Please correct the errors in the form.')
        else:
            form = HireApplicationForm()

        context = {
            'nanny': nanny,
            'form': form,
            'already_applied': False
        }

    else:
        # If the user isn't logged in or doesn't have the 'Client' role, display appropriate messages
        if not request.user.is_authenticated:
            context = {
                'nanny': nanny,
                'login_required': True,  # Notify the user they need to log in
            }
        elif request.user.role != 'Client':
            context = {
                'nanny': nanny,
                'client_required': True,  # Notify the user they need to register as a client
            }
        else:
            context = {
                'nanny': nanny,
                'already_applied': False,
            }

    return render(request, 'pages/nannies/show.html', context)

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

    return render(request, 'pages/user/client/listings/index.html', context)

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

    return render(request, 'pages/user/client/listings/create.html', context)

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

    return render(request, 'pages/user/client/listings/edit.html', context)

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

@login_required
def getJobApplicants(request):
    """
    Retrieves all job applicants who have applied for the jobs posted by the logged-in user (client).
    Displays an empty state message if no applicants are found.
    """
    # Ensure the user is logged in and is a client
    if not request.user.is_authenticated or request.user.role != 'Client':
        messages.error(request, "You are not authorized to view applicants for this job.")
        return redirect('base:getJobs')

    # Retrieve the job applications for the jobs posted by the logged-in user (client)
    job_applicants = JobApplication.objects.filter(job__client=request.user)

    # If no applicants are found, display a message
    if not job_applicants.exists():
        messages.info(request, "No applicants have applied to your jobs yet.")
    
    context = {
        'job_applicants': job_applicants
    }

    return render(request, 'pages/user/client/job-applicants/index.html', context)

@login_required
def getJobApplicantDetails(request, id):
    applicant = get_object_or_404(JobApplication, id=id)

    context = {
        'applicant': applicant
    }

    return render(request, 'pages/user/client/job-applicants/show.html', context)

@login_required
def acceptApplication(request, id):
    applicant = get_object_or_404(JobApplication, id=id)

    # Ensure that only pending applications can be accepted
    if applicant.status != 'pending':
        return JsonResponse({'status': 'error', 'message': 'Application is not pending.'})

    applicant.status = 'accepted'
    applicant.save()

    messages.success(request, 'Application has been accepted.')
    return JsonResponse({'status': 'success', 'message': 'Application accepted.'})

def rejectApplication(request, id):
    applicant = get_object_or_404(JobApplication, id=id)

    # Ensure that only pending applications can be rejected
    if applicant.status != 'pending':
        return JsonResponse({'status': 'error', 'message': 'Application is not pending.'})

    applicant.status = 'rejected'
    applicant.save()

    messages.success(request, 'Application has been rejected.')
    return JsonResponse({'status': 'success', 'message': 'Application rejected.'})

@login_required
def getHireApplications(request):
    """
    Retrieves all hire applicants who have applied for the jobs posted by the logged-in user (client).
    Displays an empty state message if no applicants are found.
    """
    # Ensure the user is logged in and is a client
    if not request.user.is_authenticated or request.user.role != 'Client':
        messages.error(request, "You are not authorized to view applicants for this job.")
        return redirect('base:getJobs')

    # Retrieve the job applications for the jobs posted by the logged-in user (client)
    applications = HireApplication.objects.filter(client=request.user)

    # If no applicants are found, display a message
    if not applications.exists():
        messages.info(request, "No hire applications you have sent yet.")
    
    context = {
        'applications': applications
    }

    return render(request, 'pages/user/client/hire-applications/index.html', context)

@login_required
def getHireApplicationDetails(request, id):
    application = get_object_or_404(HireApplication, id=id)

    context = {
        'application': application
    }

    return render(request, 'pages/user/client/hire-applications/show.html', context)

@login_required
def getJobApplications(request):
    """
    Retrieves all job applications that the logged-in Nanny has sent.
    Only accessible to users with the 'Nanny' role.
    Displays an empty state message if no applications are found.
    """
    # Ensure the user is logged in and is a Nanny
    if not request.user.is_authenticated or request.user.role != 'Nanny':
        messages.error(request, "You are not authorized to view your job applications.")
        return redirect('base:getJobs')  # Redirect to the job listings or another page as appropriate
    
    # Retrieve all job applications sent by the logged-in nanny
    applications = JobApplication.objects.filter(nanny=request.user)
    
    # If no applications are found, display a message
    if not applications.exists():
        messages.info(request, "You have not applied to any jobs yet.")
    
    context = {
        'applications': applications
    }

    return render(request, 'pages/user/nanny/job-applications/index.html', context)

@login_required
def getJobApplicationDetails(request, id):
    application = get_object_or_404(JobApplication, id=id)

    context = {
        'application': application
    }

    return render(request, 'pages/user/nanny/job-applications/show.html', context)

@login_required
def getNannyHireApplications(request):
    """
    Retrieves all job applications that the logged-in Nanny has sent.
    Only accessible to users with the 'Nanny' role.
    Displays an empty state message if no applications are found.
    """
    # Ensure the user is logged in and is a Nanny
    if not request.user.is_authenticated or request.user.role != 'Nanny':
        messages.error(request, "You are not authorized to view your job applications.")
        return redirect('base:getJobs')  # Redirect to the job listings or another page as appropriate
    
    # Retrieve all job applications sent by the logged-in nanny
    applications = HireApplication.objects.filter(nanny=request.user)
    
    # If no applications are found, display a message
    if not applications.exists():
        messages.info(request, "No one has sent hire application to you set.")
    
    context = {
        'applications': applications
    }

    return render(request, 'pages/user/nanny/hire-applications/index.html', context)

@login_required
def getNannyHireApplicationDetails(request, id):
    application = get_object_or_404(HireApplication, id=id)

    context = {
        'application': application
    }

    return render(request, 'pages/user/nanny/hire-applications/show.html', context)

@login_required
def nannyAcceptHireApplication(request, id):
    application = get_object_or_404(HireApplication, id=id)

    # Ensure that only pending applications can be accepted
    if application.status != 'pending':
        return JsonResponse({'status': 'error', 'message': 'Application is not pending.'})

    application.status = 'accepted'
    application.save()

    messages.success(request, 'Application has been accepted.')
    return JsonResponse({'status': 'success', 'message': 'Application accepted.'})

def nannyRejectHireApplication(request, id):
    application = get_object_or_404(HireApplication, id=id)

    # Ensure that only pending applications can be rejected
    if application.status != 'pending':
        return JsonResponse({'status': 'error', 'message': 'Application is not pending.'})

    application.status = 'rejected'
    application.save()

    messages.success(request, 'Application has been rejected.')
    return JsonResponse({'status': 'success', 'message': 'Application rejected.'})