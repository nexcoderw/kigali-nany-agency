from base.models import *
from django import forms
from base.models import JobPosting, JobCategory, JobStatus
from django.utils.translation import gettext_lazy as _

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