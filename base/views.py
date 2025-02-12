from django.shortcuts import render

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
    return render(request, 'Authsignup.html')