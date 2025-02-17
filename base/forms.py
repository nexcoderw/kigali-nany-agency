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