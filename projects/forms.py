from django import forms
from projects.models import Project
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
                    'engineering_start': forms.DateInput(attrs={'class': 'datepicker'}),
                    'mechanicalrelease': forms.DateInput(attrs={'class': 'datepicker'}),
                    'electricalrelease': forms.DateInput(attrs={'class': 'datepicker'}),
                    'manufacturing': forms.DateInput(attrs={'class': 'datepicker'}),
                    'finishing': forms.DateInput(attrs={'class': 'datepicker'}),
                    'assembly': forms.DateInput(attrs={'class': 'datepicker'}),
                    'integration': forms.DateInput(attrs={'class': 'datepicker'}),
                    'internalrunoff': forms.DateInput(attrs={'class': 'datepicker'}),
                    'customerrunoff': forms.DateInput(attrs={'class': 'datepicker'}),
                    'ship': forms.DateInput(attrs={'class': 'datepicker'}),
                    'installstart': forms.DateInput(attrs={'class': 'datepicker'}),
                    'installfinish': forms.DateInput(attrs={'class': 'datepicker'}),
                    'documentation': forms.DateInput(attrs={'class': 'datepicker'}),
                    }
class RegisterExtendedForm(UserCreationForm):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
