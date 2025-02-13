from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile

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

def Signup(request):
    print("🔍 Signup view triggered!")  # Debugging
    if request.method == "POST":
        print("✅ Signup form submitted!")  # Debugging

        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        role = request.POST["role"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("base:signup")

        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("base:signup")

        user = UserProfile.objects.create_user(username=username, email=email, phone=phone, role=role, password=password)
        messages.success(request, "Account created successfully! You can now log in.")
        return redirect("base:login")

    return render(request, "Auth/signup.html")



def Login(request):
    print("🔍 Login view triggered!")
    if request.method == "POST":
        print("✅ Login form submitted!")  # Debugging
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("base:dashboard")  # Redirect to dashboard instead of home
        else:
            messages.error(request, "Invalid username or password")
            return redirect("base:login")

    return render(request, "Auth/login.html")


def Logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("base:logout")  # Redirect to login after logout

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