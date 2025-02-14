from django.shortcuts import render

def home(request):
    return render(request, 'pages/index.html')

def dashboard(request):
    return render(request, 'pages/user/dashboard.html')

def getJobListings(request):
    return render(request, 'pages/user/listings/index.html')

def addJobListing(request):
    return render(request, 'pages/user/listings/create.html')

def editJobListing(request):
    return render(request, 'pages/user/listings/edit.html')

def deleteJobListing(request):
    pass