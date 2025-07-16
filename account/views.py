import random
import logging
from base.forms import *
from base.models import *
from account.forms import *
from account.models import *
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash

logger = logging.getLogger(__name__)

def userLogin(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, _("You have been logged out because you accessed the login page while already logged in."))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            auth_login(request, user)
            messages.success(request, _("Welcome back! You have successfully logged in."))
            return redirect(reverse('base:home'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            messages.error(request, _("Please address the errors below and try again."))
    else:
        form = LoginForm()

    settings = Setting.objects.first()

    context = {
        'form': form,
        'settings': settings
    }

    return render(request, 'pages/auth/login.html', context)

def userLogout(request):
    logout(request)
    messages.success(request, _("You have been successfully logged out."))

    return redirect('auth:login')

def userRegister(request):
    if request.user.is_authenticated:
        return redirect(reverse('base:home'))
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save the user yet
            # Set the password manually to ensure it's hashed
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Log the user in immediately after saving
            auth_login(request, user)
            messages.success(request, _("Your account has been created successfully and you are now logged in."))
            return redirect(reverse('base:home'))  # Or wherever you want to redirect
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            messages.error(request, _("Please correct the errors below."))
    else:
        form = RegisterForm()

    settings = Setting.objects.first()

    context = {
        'form': form,
        'settings': settings
    }

    return render(request, 'pages/auth/register.html', context)

@login_required
def userProfile(request):
    """
    View to allow users to update their profile information (User, Nanny, or Client).
    """
    user = request.user

    # Check if the user is a Nanny or Client to determine which profile to update
    if user.role == 'Nanny':
        profile = get_object_or_404(NannyProfile, user=user)
        profile_form = NannyProfileForm(request.POST or None, instance=profile)
    elif user.role == 'Client':
        profile = get_object_or_404(ClientProfile, user=user)
        profile_form = ClientProfileForm(request.POST or None, instance=profile)
    else:
        profile_form = None
    
    user_form = UserUpdateForm(request.POST or None, instance=user)

    # If the forms are valid, save the data
    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('account:update_profile')
        else:
            messages.error(request, "Please correct the errors below.")

    settings = Setting.objects.first()

    context = {
        'user_form': user_form,
        'settings': settings,
        'profile_form': profile_form,
    }

    return render(request, 'pages/auth/profile.html', context)

def generate_otp():
    """
    Generate a random 7-digit OTP.
    """
    return str(random.randint(1000000, 9999999))


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            otp = generate_otp()  # your generate_otp helper function
            user.reset_otp = otp
            user.otp_created_at = timezone.now()
            user.save()

            # Send the OTP via email (ensure your email settings are correct)
            subject = 'Password Reset OTP'
            message = f'Your password reset OTP is: {otp}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                messages.success(request, "An OTP has been sent to your email address. Please check your inbox.")
                # Store the email in session so it can be used in the confirmation form
                request.session['reset_email'] = email
                return redirect('auth:forgetPasswordConfirm')
            except Exception as e:
                messages.error(request, "Failed to send OTP email. Please try again later.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordResetRequestForm()

    settings = Setting.objects.first()

    context = {
        'form': form,
        'settings': settings,
        'step': 'request'
    }

    return render(request, 'pages/auth/forget-password.html', context)

def password_reset_confirm(request):
    if request.method == 'POST':
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            # Clear the OTP fields
            user.reset_otp = None
            user.otp_created_at = None
            user.save()
            messages.success(request, "Your password has been reset successfully. Please log in with your new password.")
            # Remove the email from session after successful reset
            request.session.pop('reset_email', None)
            return redirect('auth:login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # Retrieve the email from session and set it as initial data
        email = request.session.get('reset_email', '')
        form = PasswordResetConfirmForm(initial={'email': email})

    settings = Setting.objects.first()

    context = {
        'form': form,
        'settings': settings,
        'step': 'confirm'
    }

    return render(request, 'pages/auth/forget-password.html', context)