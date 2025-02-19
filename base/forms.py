from base.models import *
from django import forms
from django.utils.translation import gettext_lazy as _
from base.models import JobPosting, JobCategory, JobStatus
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

class JobPostingForm(forms.ModelForm):
    """
    Form for creating and editing job postings.
    """

    class Meta:
        model = JobPosting
        fields = ['title', 'description', 'category', 'status', 'salary', 'location', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': _('Enter job title'),
                'required': 'required',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': _('Provide a detailed description'),
                'required': 'required',
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'required': 'required',
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'required': 'required',
                'class': 'form-control'
            }),
            'salary': forms.NumberInput(attrs={
                'placeholder': _('Enter salary'),
                'class': 'form-control'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': _('Enter job location'),
                'class': 'form-control'
            }),
            'start_date': forms.DateInput(attrs={
                'placeholder': _('Enter start date'),
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'placeholder': _('Enter end date (optional)'),
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = JobCategory.choices
        self.fields['status'].choices = JobStatus.choices

class JobApplicationForm(forms.ModelForm):
    """
    Form for creating and editing job postings.
    """
    # Set the initial value for availability to today
    availability = forms.DateField(initial=timezone.now().date(), widget=forms.DateInput(attrs={
        'type': 'date',  # Ensure it's rendered as a date picker
        'required': 'required',
        'class': 'form-control',
        'min': timezone.now().date()  # Ensure no past dates are selectable
    }))
    
    class Meta:
        model = JobApplication
        fields = ['experience', 'availability', 'cover_letter']
        widgets = {
            'experience': forms.TextInput(attrs={
                'placeholder': _('Describe your experience in this field'),
                'required': 'required',
                'class': 'form-control'
            }),
            'cover_letter': forms.Textarea(attrs={
                'placeholder': _('Cover letter'),
                'required': 'required',
                'class': 'form-control'
            }),
        }

class HireApplicationForm(forms.ModelForm):
    """
    Form for creating and editing a hire application from a client to a nanny.
    """
    class Meta:
        model = HireApplication
        fields = [
            'job_title', 
            'description', 
            'expected_start_date', 
            'expected_end_date', 
            'expected_salary', 
            'work_schedule', 
            'additional_requirements'
        ]
        widgets = {
            'job_title': forms.TextInput(attrs={
                'placeholder': _('Enter job title'),
                'required': 'required',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': _('Describe the job details'),
                'required': 'required',
                'class': 'form-control',
                'rows': 4
            }),
            'expected_start_date': forms.DateInput(attrs={
                'placeholder': _('Select expected start date'),
                'class': 'form-control',
                'type': 'date',
                'required': 'required'
            }),
            'expected_end_date': forms.DateInput(attrs={
                'placeholder': _('Select expected end date'),
                'class': 'form-control',
                'type': 'date',
                'required': 'required'
            }),
            'expected_salary': forms.NumberInput(attrs={
                'placeholder': _('Enter expected salary'),
                'required': 'required',
                'class': 'form-control'
            }),
            'work_schedule': forms.Textarea(attrs={
                'placeholder': _('Provide a detailed work schedule'),
                'required': 'required',
                'class': 'form-control',
                'rows': 4
            }),
            'additional_requirements': forms.Textarea(attrs={
                'placeholder': _('Provide any additional requirements or comments'),
                'class': 'form-control',
                'rows': 4
            }),
        }

    def clean_expected_salary(self):
        """
        Custom validation for expected_salary to ensure it is a positive number.
        """
        salary = self.cleaned_data.get('expected_salary')
        if salary and salary <= 0:
            raise forms.ValidationError(_('Salary must be a positive number'))
        return salary

class UserUpdateForm(UserChangeForm):
    """
    Form to update the user profile (name, email, phone number, password).
    """
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank if you don't want to change the password")

    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'phone_number', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class NannyProfileForm(forms.ModelForm):
    """
    Form for updating nanny profile details.
    """
    class Meta:
        model = NannyProfile
        fields = [
            'date_of_birth', 
            'biography', 
            'years_of_experience', 
            'certifications', 
            'languages_spoken', 
            'previous_employers', 
            'hourly_rate', 
            'preferred_working_hours', 
            'availability_notes'
        ]
        widgets = {
            'biography': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'certifications': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'languages_spoken': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'previous_employers': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'preferred_working_hours': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'availability_notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

class ClientProfileForm(forms.ModelForm):
    """
    Form for updating client profile details.
    """
    class Meta:
        model = ClientProfile
        fields = [
            'company_name', 
            'company_description', 
            'address'
        ]
        widgets = {
            'company_description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }