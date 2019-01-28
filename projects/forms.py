from django import forms
from projects.models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['employees']
        widgets = {
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
                    'documentation': forms.DateInput(attrs={'class': 'datepicker'})

                    }