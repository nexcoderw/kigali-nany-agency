from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')

def services(request):
    return render(request, 'pages/services.html')

def getJobs(request):
    return render(request, 'pages/jobs/index.html')

def showJob(request):
    return render(request, 'pages/jobs/show.html')

def contact(request):
    return render(request, 'pages/contact.html')
def Login(request):
    return render(request, 'Auth/login.html')
def Signup(request):
    return render(request, 'Auth/signup.html')

#Dashboard pages
def login_redirect(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required(login_url="/login")
def UserDashboard(request):
    return render(request, 'Dashboard/userindex.html')

@login_required(login_url="/login")
def UserBookings(request):
    return render(request, 'Dashboard/userbookings.html')