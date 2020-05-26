from django import forms
from projects.models import Project
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('lastupdated', \
                    'Status', \
                    'iscurrent', \
                    'Slippage', \
                    'scheduled', \
                    )

        widgets = {
                    'projectname': forms.TextInput(attrs={'class': 'special','size': '50'}),
                    'Comments': forms.Textarea(attrs={"rows":5, "cols":40}),
                    'engineering_start': forms.DateInput(attrs={'class': 'datepicker'}),
                    'MilestoneOne': forms.DateInput(attrs={'class': 'datepicker'}),
                    'MilestoneTwo': forms.DateInput(attrs={'class': 'datepicker'}),
                    'MilestoneThree': forms.DateInput(attrs={'class': 'datepicker'}),
                    'MilestoneFour': forms.DateInput(attrs={'class': 'datepicker'}),
                    'MilestoneFive': forms.DateInput(attrs={'class': 'datepicker'}),
                    'MilestoneSix': forms.DateInput(attrs={'class': 'datepicker'}),
                    'MilestoneSeven': forms.DateInput(attrs={'class': 'datepicker'}),
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
