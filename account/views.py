from account.forms import *
from account.models import *
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash

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

    context = {
        'form': form
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

    context = {
        'form': form,
    }

    return render(request, 'pages/auth/register.html', context)

@login_required
def userProfile(request):
    user = request.user

    if request.method == 'POST':
        if 'profile_form' in request.POST:
            profile_form = UserProfileForm(request.POST, request.FILES, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profil mis à jour avec succès.')
                return redirect('auth:userProfile')
            else:
                password_form = PasswordChangeForm(user=user)
        elif 'password_form' in request.POST:
            password_form = PasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, 'Mot de passe modifié avec succès. Veuillez vous reconnecter.')
                logout(request)
                return redirect('auth:login')
            else:
                profile_form = UserProfileForm(instance=user)
    else:
        profile_form = UserProfileForm(instance=user)
        password_form = PasswordChangeForm(user=user)

    context = {
        'profile_form': profile_form,
        'password_form': password_form
    }

    return render(request, 'pages/auth/profile.html', context)