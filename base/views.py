from django.shortcuts import render

def home(request):
    return render(request, 'pages/index.html')

def dashboard(request):
    return render(request, 'pages/user/dashboard.html')

def getJobListings(request):
    return render(request, 'pages/user/listing/index.html')