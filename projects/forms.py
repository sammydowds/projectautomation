from django import forms
from projects.models import Project
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('lastupdated','Status', 'iscurrent')
        widgets = {
                    'projectname': forms.TextInput(attrs={'class': 'special','size': '50'}),
                    'Comments': forms.Textarea(attrs={"rows":5, "cols":40}),
                    'engineering_start': forms.DateInput(attrs={'class': 'datepicker'}),
                    'Mechanical_Release': forms.DateInput(attrs={'class': 'datepicker'}),
                    'Electrical_Release': forms.DateInput(attrs={'class': 'datepicker'}),
                    'Manufacturing': forms.DateInput(attrs={'class': 'datepicker'}),
                    'Finishing': forms.DateInput(attrs={'class': 'datepicker'}),
                    'Assembly': forms.DateInput(attrs={'class': 'datepicker'}),
                    'Integration': forms.DateInput(attrs={'class': 'datepicker'}),
                    'Internal_Runoff': forms.DateInput(attrs={'class': 'datepicker'}),
                    'Customer_Runoff': forms.DateInput(attrs={'class': 'datepicker'}),
                    'Ship': forms.DateInput(attrs={'class': 'datepicker'}),
                    'Install_Start': forms.DateInput(attrs={'class': 'datepicker'}),
                    'Install_Finish': forms.DateInput(attrs={'class': 'datepicker'}),
                    'Documentation': forms.DateInput(attrs={'class': 'datepicker'}),
                    }


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('Comments',)
        widgets = {
        'Comments': forms.Textarea(attrs={"rows":5, "cols":40}),

        }

class RegisterExtendedForm(UserCreationForm):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
