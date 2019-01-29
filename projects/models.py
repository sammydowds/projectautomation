from django.db import models


# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Project(models.Model):
    projectnumber = models.IntegerField()
    projectname = models.CharField(max_length=100)
    mechanicalrelease = models.DateField(null = True)
    electricalrelease = models.DateField(null = True)
    manufacturing = models.DateField(null = True)
    finishing = models.DateField(null = True)
    assembly = models.DateField(null = True)
    integration = models.DateField(null = True)
    internalrunoff = models.DateField(null = True)
    customerrunoff = models.DateField(null = True)
    ship = models.DateField(null = True)
    installstart = models.DateField(null = True)
    installfinish = models.DateField(null = True)
    documentation = models.DateField(null = True)
    offtrack = models.BooleanField(null = True)
    onwatch = models.BooleanField(null = True)
    iscurrent = models.BooleanField(null = True)
    employees = models.ManyToManyField(Employee)

    def __str__(self):
        return self.projectname





    # projectnumber = forms.IntegerField(label = "Project Number")
    # projectname = forms.CharField(label = "Project Name", max_length=30)
    # offtrack = forms.BooleanField(label = "Off Track")
    # onwatch = forms.BooleanField(label = "On Watch")
    # mechanicalrelease = forms.DateField(label = "Mechanical Release")
    # electricalrelease = forms.DateField(widget=forms.SelectDateWidget(),label = "Electrical Release")
    # manufacturing = forms.DateField(widget=forms.SelectDateWidget(),label = "Manufacturing")
    # finishing = forms.DateField(widget=forms.SelectDateWidget(),label = "Finishing")
    # assembly = forms.DateField(widget=forms.SelectDateWidget(),label = "Assembly")
    # integration = forms.DateField(widget=forms.SelectDateWidget(),label = "Integration")
    # internalrunoff = forms.DateField(widget=forms.SelectDateWidget(),label = "Internal Runoff")
    # customerrunoff = forms.DateField(widget=forms.SelectDateWidget(),label = "Customer Runoff")
    # ship = forms.DateField(widget=forms.SelectDateWidget(),label = "Ship Date")
    # installstart = forms.DateField(widget=forms.SelectDateWidget(),label = "Install Start")
    # installfinish = forms.DateField(widget=forms.SelectDateWidget(),label = "Install Finish")
    # documentation = forms.DateField(widget=forms.SelectDateWidget(),label = "Documenation")
